from CoolProp.CoolProp import PropsSI
import azure.functions as func
import json
from math import isnan


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        p1 = req_body.get('p1')
        v1 = req_body.get('v1')
        p2 = req_body.get('p2')
        v2 = req_body.get('v2')
        f = req_body.get('f')

    if p1 and v1 and p2 and v2 and f:
        res = {
            "MolarMass": PropsSI("MOLARMASS", p1, v1, p2, v2, f),
            "Temperature": PropsSI("T", p1, v1, p2, v2, f),
            "Pressure": PropsSI("P", p1, v1, p2, v2, f),
            "SpecificMassDensity": 1.0/PropsSI("DMASS", p1, v1, p2, v2, f),
            "SpecificMolarDensity": 1.0/PropsSI("DMOLAR", p1, v1, p2, v2, f),
            "SpecificMassInternalEnergy": PropsSI("UMASS", p1, v1, p2, v2, f),
            "SpecificMolarInternalEnergy": PropsSI("UMOLAR", p1, v1, p2, v2, f),
            "SpecificMassEnthalpy": PropsSI("HMASS", p1, v1, p2, v2, f),
            "SpecificMolarEnthalpy": PropsSI("HMOLAR", p1, v1, p2, v2, f),
            "SpecificMassEntropy": PropsSI("SMASS", p1, v1, p2, v2, f),
            "SpecificMolarEntropy": PropsSI("SMOLAR", p1, v1, p2, v2, f),
            "ThermalConductivity": PropsSI("CONDUCTIVITY", p1, v1, p2, v2, f),
            "MassConstantPressureSpecificHeat": PropsSI("CPMASS", p1, v1, p2, v2, f),
            "MolarConstantPressureSpecificHeat": PropsSI("CPMOLAR", p1, v1, p2, v2, f),
            "MassConstantVolumeSpecificHeat": PropsSI("CVMASS", p1, v1, p2, v2, f),
            "MolarConstantVolumeSpecificHeat": PropsSI("CVMOLAR", p1, v1, p2, v2, f),
            "PrandtlNumber": PropsSI("PRANDTL", p1, v1, p2, v2, f),
            "Viscosity": PropsSI("VISCOSITY", p1, v1, p2, v2, f),
            "isCalculated": True
        }

        for key in res.keys:
            if key != "isCalculated" and not isnan(res[key]):
                res["isCalculated"] = False

        return func.HttpResponse(json.dumps(res))
    else:
        return func.HttpResponse(
            "Please pass a valid input on the query string or in the request body",
            status_code=400
        )
