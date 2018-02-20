
schema MillDemoState
    Float32 f_x,
    Float32 f_y,
    Float32 delta_x,
    Float32 delta_y
end

schema MillDemoAction
    Float32 {-30.0:30.0} u_x,
    Float32 {-20.0:20.0} u_y
end

schema MillDemoConfig
    Int8 dummy
end

concept mill is estimator
   predicts (MillDemoAction)
   follows input(MillDemoState)
   feeds output
   experimental
      algorithm_ => "TRPO" : "TRPO"
   end
end

simulator simulink_sim(MillDemoConfig)
    action (MillDemoAction)
    state (MillDemoState)
end

curriculum my_curriculum
    train mill
    with simulator simulink_sim
    objective milldemo_smooth
        lesson my_first_lesson
            configure
                constrain dummy with Int8{-1}
            until
                maximize milldemo_smooth
end
