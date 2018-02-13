
schema CartpoleState
    Float32 theta,
    Float32 dtheta,
    Float32 x,
    Float32 dx
end

schema CartpoleAction
    Float32 {-10.0:10.0} f
end

schema CartpoleConfig
    Int8 dummy
end

concept balance is estimator
   predicts (CartpoleAction)
   follows input(CartpoleState)
   feeds output
    experimental
        algorithm_ => "TRPO" : "TRPO"
    end
end

simulator simulink_sim(CartpoleConfig)
    action (CartpoleAction)
    state (CartpoleState)
end

curriculum my_curriculum
    train balance
    with simulator simulink_sim
    objective cartpole_balance
        lesson my_first_lesson
            configure
                constrain dummy with Int8{-1}
            until
                maximize cartpole_balance
end
