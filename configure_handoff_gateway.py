
    GATEWAY_NAME = 'edit-name-here'
    ENTERPRISE_ID = 1
    EDGE_ID = 1

    # Get Gateway logicalId (may also use, e.g. network/getNetworkGateways)
    gateways = client.call('network/getNetworkGateways', {})
    gateway = [g for g in gateways if g["name"] == GATEWAY_NAME][0]
    logicalId = gateway['logicalId']
    print("logicalId=%s" % (logicalId))

    # Get Edge data
    params = {"enterpriseId": ENTERPRISE_ID, "edgeId": EDGE_ID}
    # submit edge/getEdgeConfigurationStack
    res = client.call('edge/getEdgeConfigurationStack', params)

    edgeSpecificProfile = res[0]
    deviceSettings = [m for m in edgeSpecificProfile["modules" ] if m["name"] == "deviceSettings"][0]
    data = deviceSettings["data"]
    moduleId = deviceSettings["id"]
    segments = data["segments"]
    print("moduleId %d name=%s" % (moduleId, deviceSettings["name"]))

    # Add handoff gateway to global segment
    seg = segments[0]
    seg["handOffGateways"] = {}
    handOffGateways = seg["handOffGateways"]
    if "gateways" in handOffGateways:
        del handOffGateways["gateways"]
    handOffGateways["override"] = True
    handOffGateways["gatewayList"] = [{"logicalId":logicalId}]
    handOffGateways["autoSelect"] = False

    # Update configuration module data
    params = {"enterpriseId": ENTERPRISE_ID,
              "id": moduleId,
              "_update": {"data": data}}
    #submit configuration/getConfigurationModules
    res = client.call('configuration/updateConfigurationModule', params)
