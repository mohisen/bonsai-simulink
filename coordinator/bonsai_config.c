#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <json-glib/json-glib.h>
#include <json-glib/json-gobject.h>

#include <curl/curl.h>

#include "tmwtypes.h"

#include "rtwtypes.h"

real_T* config_cache = NULL;

extern int g_debug;
extern int g_id;

extern JsonReader *
post_json(JsonBuilder * req, JsonParser ** parserp);

void
bonsai_init(int_T numConfigs, real_T *xC) {
    if (config_cache == NULL) {
        config_cache = malloc(sizeof(real_T) * numConfigs);
        if (g_debug) {
            fprintf(stderr, "bonsai_init starting w/ %d config\n", numConfigs);
        }

        JsonBuilder *req = json_builder_new();

        json_builder_begin_object(req);

        json_builder_set_member_name(req, "jsonrpc");
        json_builder_add_string_value(req, "2.0");

        json_builder_set_member_name(req, "id");
        json_builder_add_int_value(req, g_id++);

        json_builder_set_member_name(req, "method");
        json_builder_add_string_value(req, "getconfig");

        json_builder_set_member_name(req, "params");
        json_builder_begin_object(req);
        json_builder_end_object (req);

        json_builder_end_object (req);

        JsonParser * parser;
        JsonReader * rsp = post_json(req, &parser);

        json_reader_read_member(rsp, "result");
        json_reader_read_member(rsp, "config");

        int n = json_reader_count_elements(rsp);
        if (n != numConfigs) {
            fprintf(stderr, "got %d configs instead of %d", n, numConfigs);
            exit(1);
        }

        for (size_t ii = 0; ii < numConfigs; ++ii) {
            json_reader_read_element(rsp, ii);
            config_cache[ii] = json_reader_get_double_value(rsp);
            json_reader_end_element(rsp);
        }

        json_reader_end_member(rsp); // config
        json_reader_end_member(rsp); // result

        g_object_unref(rsp);
        g_object_unref(parser);
    }

    for (size_t ii = 0; ii < numConfigs; ++ii) {
        xC[ii] = config_cache[ii];
    }

    if (g_debug) {
        fprintf(stderr, "bonsai_init finished\n");
    }
    
    return;
}


