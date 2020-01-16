import pyhapi as ph
import numpy as np

def main():
    session     = ph.HSessionManager.GetOrCreateDefaultSession()

    #load hda asset and instantiate
    hdaAsset    = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node  = hdaAsset.Instantiate(node_name = "TestObject").Cook()
    asset_geos  = asset_node.GetDisplayGeos()

    for geo in asset_geos:
        print("Geo {0} has attribute {1}".format(geo, geo.GetAttribNames()))

    print(asset_geos[0].GetAttribData(ph.AttributeType.POINT, "P"))

    session.SaveHIP("modifiedScene.hip")


if __name__ == "__main__":
    main()