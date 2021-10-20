import dataikuapi
import radon.raw as cc_raw
import radon.visitors as cc_visitors
from helpers import trigger_scenario


def test_scenario(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    # Check that there is at least one scenario TEST_XXXXX & one TEST_SMOKE
    scenarios = project.list_scenarios()
    test_scenario = False
    smoketest_scenario = False

    smoke_scenario_run = trigger_scenario(scenario["TEST_SMOKE"])
    unit_scenario_run = trigger_scenario(scenario["TEST_UNIT"])  # actual details of run after checking for trigger

    while True:
        smoke_scenario_run.refresh()
        unit_scenario_run.refresh()

        if not (smoke_scenario_run.running and unit_scenario_run):
            if smoke_scenario_run.outcome == "SUCCESS":
                smoketest_scenario = True
            else:
                print(f"Smoke Test Error was: {moke_scenario_run.get_details().first_error_details}")
            if smoke_scenario_run.outcome == "SUCCESS":
                unit_scenario_run = True
            else:
                print(f"Unit Test Error was: {smoke_scenario_run.get_details().first_error_details}")
            break

    assert unit_scenario_run, "You need at least one test scenario (name starts with 'TEST_')"
    assert smoketest_scenario, "You need at least one smoke test scenario (name 'TEST_SMOKE')"


def test_coding_recipes_complexity(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    recipes = project.list_recipes()
    for recipe in recipes:
        if recipe["type"] == "python":
            print(recipe)
            payload = project.get_recipe(recipe["name"]).get_settings().get_payload()
            code_analysis = cc_raw.analyze(payload)
            print(code_analysis)
            assert code_analysis.loc < 2000
            assert code_analysis.lloc < 50
            v = cc_visitors.ComplexityVisitor.from_code(payload)
            assert v.complexity < 21, "Code complexity of recipe " + recipe[
                "name"] + " is too complex: " + v.complexity + " > max value (21)"
