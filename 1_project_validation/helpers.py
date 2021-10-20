

def trigger_scenario(
        scenario_name: dataikuapi.dss.scenario.DSSScenario
):
    scenario_fire = scenario_name.run() # manual trigger
    scenario_run = scenario_fire() #
    return scenario_run
