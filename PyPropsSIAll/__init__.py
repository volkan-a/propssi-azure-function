from CoolProp.CoolProp import PropsSI
import azure.functions as func
import json
from math import isnan
from uuid import uuid4
from enum import Enum


class Property(Enum):
    PRESSURE = 0
    TEMPERATUE = 1
    DENSITY = 2
    SPECIFIC_INTERNAL_ENERGY = 3
    SPECIFIC_ENTHALPY = 4
    SPECIFIC_ENTROPY = 5
    VAPOR_FRACTION = 6


property_names = ("P", "T", "D", "U", "H", "S", "Q")


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        p1 = property_names[req_body.get('Prop1')]
        v1 = req_body.get('Value1')
        p2 = property_names[req_body.get('Prop2')]
        v2 = req_body.get('Value2')
        f = req_body.get('Fluid')

    if p1 and v1 and p2 and v2 and f:
        try:
            res = {
                "id": uuid4().int,
                "MolarMass": PropsSI("MOLARMASS", p1, v1, p2, v2, f),
                "Temperature": PropsSI("T", p1, v1, p2, v2, f),
                "Pressure": PropsSI("P", p1, v1, p2, v2, f),
                "SpecificMassVolume": 1.0/PropsSI("DMASS", p1, v1, p2, v2, f),
                "SpecificMolarVolume": 1.0/PropsSI("DMOLAR", p1, v1, p2, v2, f),
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
                "VaporFraction": PropsSI("Q", p1, v1, p2, v2, f),
                "isCalculated": True
            }
        except:
            return func.HttpResponse('{"ErrorMessage": "CoolProp error!"}', status_code=400)

        for key in res.keys():
            if key != "isCalculated" and isnan(res[key]):
                res["isCalculated"] = False

        return func.HttpResponse(json.dumps(res))
    else:
        return func.HttpResponse(
            '{"ErrorMessage": "Please pass a valid input on the query string or in the request body"}',
            status_code=400
        )
