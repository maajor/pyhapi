import pyhapi as ph
import numpy as np

def log_childnodes(asset_node):
    print("Child nodes include: {0}".format(",".join([node.Name for node in asset_node.GetChildNodes()])))

def main():
    session     = ph.HSessionManager.GetOrCreateDefaultSession()

    #load hda asset and instantiate
    hdaAsset    = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node  = hdaAsset.Instantiate(node_name = "Processor").Cook()
    log_childnodes(asset_node)

    #create a sop node, set input
    another_box = ph.HNode(session, "geo", "ProgrammaticBox", parent_node = asset_node)
    input_node  = another_box\
    		.ConnectNodeInput(asset_node.GetChildNodes()[0])\
		    .Cook()\
		    .GetNodeInput(0)
    print("ProgrammaticBox's input node is {0}".format(input_node.Name))
    log_childnodes(asset_node)

    #delete sop node
    another_box\
    		.DisconnectNodeInput(0)\
    		.Delete()
    log_childnodes(asset_node)

    session.SaveHIP("modifiedScene.hip")


if __name__ == "__main__":
    main()