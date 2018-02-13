// Copyright (C) 2017 Bonsai AI, Inc.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <json-glib/json-glib.h>
#include <json-glib/json-gobject.h>

#include <curl/curl.h>

#include "tmwtypes.h"

#include "rtwtypes.h"

static const char * PORTENV = "BONSAI_COORDINATOR_PORT";
static const char * DEBUGENV = "BONSAI_DEBUG";

int g_debug = 0;
int g_id = 0;

static CURL * g_curl = NULL;
static int g_steps = 0;

static void check_init() {
    // If we are already initialized, we're done.
    if (g_curl) {
        return;
    }

    char const * debugstr = getenv(DEBUGENV);
    if (!debugstr) {
        g_debug = 0;
    } else {
        g_debug = 1;
    }
  
    char const * portstr = getenv(PORTENV);
    if (!portstr) {
        fprintf(stderr, "missing %s env variable\n", PORTENV);
        goto failed;
    }
  
    curl_global_init(CURL_GLOBAL_ALL);
  
    g_curl = curl_easy_init();
    if (!g_curl) {
        fprintf(stderr, "curl_easy_init failed\n");
        goto failed;
    }

    char urlbuf[1024];
    snprintf(urlbuf, sizeof(urlbuf), "http://localhost:%s/", portstr);
  
	curl_easy_setopt(g_curl, CURLOPT_URL, urlbuf);
 
    return;
  
 failed:
    curl_global_cleanup();
    exit(1);
}

typedef struct MemoryStruct_s {
    char * memory;
    size_t size;
} MemoryStruct_t;

static size_t
WriteMemoryCallback(void * contents, size_t size, size_t nmemb, void * userp) {
    size_t realsize = size * nmemb;
    MemoryStruct_t * mem = (MemoryStruct_t*) userp;
    mem->memory = realloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory == NULL) {
        fprintf(stderr, "realloc failed");
        exit(1);
    }

    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

JsonReader *
post_json(JsonBuilder * req, JsonParser ** parserp) {
    check_init();
    
    JsonGenerator *gen = json_generator_new();
    JsonNode * root = json_builder_get_root(req);
    json_generator_set_root(gen, root);
    gchar *postbody = json_generator_to_data (gen, NULL);

    MemoryStruct_t rsp;
    rsp.memory = malloc(1);	// Will be grown as needed.
    rsp.size = 0;

    struct curl_slist * hdrs = NULL;
    hdrs = curl_slist_append(hdrs, "Accept: application/json");
    hdrs = curl_slist_append(hdrs, "Content-Type: application/json");
    curl_easy_setopt(g_curl, CURLOPT_HTTPHEADER, hdrs);

    curl_easy_setopt(g_curl, CURLOPT_POSTFIELDS, postbody);
    curl_easy_setopt(g_curl, CURLOPT_POSTFIELDSIZE, (long)strlen(postbody));
    
    curl_easy_setopt(g_curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(g_curl, CURLOPT_WRITEDATA, (void *) &rsp);

    if (g_debug) {
        fprintf(stderr, "post_json: req: %s\n", postbody);
    }
    
    CURLcode res = curl_easy_perform(g_curl);
    if(res != CURLE_OK) {
        fprintf(stderr, "bonsai_init: curl_easy_perform failed: %s\n",
                curl_easy_strerror(res));
        curl_global_cleanup();
        exit(1);
    }

    if (g_debug) {
        fprintf(stderr, "post_json: rsp: %s\n", rsp.memory);
    }
    
    g_free(postbody);
    json_node_free(root);
    g_object_unref(gen);
    g_object_unref(req);

    *parserp = json_parser_new();
    json_parser_load_from_data(*parserp, rsp.memory, -1, NULL);

    JsonReader *reader = json_reader_new(json_parser_get_root(*parserp));
    
    free(rsp.memory);
    
    return reader;
}

void
bonsai_step(int_T numInputs, real_T *xI, int_T numOutputs, real_T *xO) {

  // This routine is called by TLC Outputs

    if (g_debug) {
        fprintf(stderr, "bonsai_step starting, time %f\n", *time);
    }
    
    ++g_steps;
    
    JsonBuilder *req = json_builder_new();

    json_builder_begin_object(req);

    json_builder_set_member_name(req, "jsonrpc");
    json_builder_add_string_value(req, "2.0");
    
    json_builder_set_member_name(req, "id");
    json_builder_add_int_value(req, g_id++);

    json_builder_set_member_name(req, "method");
    json_builder_add_string_value(req, "step");

    gboolean isterminal = FALSE;
    json_builder_set_member_name(req, "params");
    {
        json_builder_begin_object(req);
        
        json_builder_set_member_name(req, "state");
        {
            json_builder_begin_array(req);

            for (size_t ii = 0; ii < numInputs; ++ii) {
                json_builder_add_double_value(req, xI[ii]);
            }
            
            json_builder_end_array(req);
        }
		
        json_builder_end_object (req);
    }
    
    json_builder_end_object (req);

    if (g_debug) {
        fprintf(stderr, "bonsai_step post starting\n");
    }
    
    JsonParser * parser;
    JsonReader * rsp = post_json(req, &parser);

    // {"id": 524, "jsonrpc": "2.0", "result": {"action": [ 1.0 ]}}

    json_reader_read_member(rsp, "result");
    json_reader_read_member(rsp, "action");

    if (json_reader_count_elements(rsp) == 0) {
        // If the action array is zero sized we are being signaled to terminate.
        exit(0);
    }

    for (size_t ii = 0; ii < numOutputs; ++ii) {
        json_reader_read_element(rsp, ii);
        xO[ii] = json_reader_get_double_value(rsp);
        json_reader_end_element(rsp);
    }

    json_reader_end_member(rsp); // action
    json_reader_end_member(rsp); // result
        
    g_object_unref(rsp);
    g_object_unref(parser);

    if (g_debug) {
        fprintf(stderr, "bonsai_step finished\n");
    }
}
