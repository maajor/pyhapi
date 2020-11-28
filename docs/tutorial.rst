Tutorial
======================

Create a session and instantiate HDA
--------------------------------------------

You can start houdini engine with code, and instantiate your houdini digital asset.

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="Processor").cook()

Connect and disconnect nodes
--------------------------------------------

You can instantiate any operator in houdini engine's session, connect and disconnect any of them.

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="Processor")

    #create a sop node, set input
    another_box = ph.HNode(session, "geo", "ProgrammaticBox", parent_node=asset_node)
    input_node = another_box\
    		.connect_node_input(asset_node.get_child_nodes()[0])\
		    .cook()\
		    .get_node_input(0)
    print("ProgrammaticBox's input node is {0}".format(input_node.name))

    #delete sop node
    another_box\
    		.disconnect_node_input(0)\
    		.delete()

Set and get parameter of node 
--------------------------------------------

You can get and set all paramters on an node's interface, even press a button

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/SideFX_spaceship.otl")
    asset_node = hda_asset.instantiate(node_name="Spaceship")

    #Query node's parameters
    for name in asset_node.get_param_names():
        print("Query param: {0} has value: {1}".format(name, asset_node.get_param_value(name)))

    #Set node's parameters
    asset_node.set_param_value("seed", 1.0)
    asset_node.set_param_value("rop_geometry1_sopoutput", "$HIP/spaceship.obj")

    #Press button
    asset_node.press_button("rop_geometry1_execute", status_report_interval=1.0)

    hda_asset = ph.HAsset(session, "hda/dummy_params.hda")
    asset_node = hda_asset.instantiate(node_name="params")

    #Setting multi-size parameters
    asset_node.set_param_value("intvec3", [1, 1, 1])
    asset_node.set_param_value("vec4", [0.5, 0.6, 0.7, 0.8])
    asset_node.set_param_value("color", [0.3, 0.4, 0.5])
    asset_node.set_param_value("toggle", True)
    asset_node.set_param_value("strings5", ["str0", "str1", "str2", "str3", "str4"])

    #Getting/Setting choice
    parm = asset_node.get_param("ordermenu")
    print("{0} is type {1}, has choice {2}".format(parm.get_name(), parm, parm.get_choice_values()))
    parm.set_value(index=1)


Save/Load HIP file
--------------------------------------------

You can save current session to hip file for debug, as well as load an hip file into session.

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()
    session.save_hip("debug.hip")
    session.load_hip("debug.hip")


Marshall Data
--------------------------------------------

You can marshal curve and mesh data in numpy format in/out houdini engine.
Data should be in numpy.ndarray type.

Marshall Curve In
++++++++++++++++++++++++++++++++++++++++++++

Vertices should be in shape (num_vertices, 3)

.. code-block:: python

    import logging
    import numpy as np
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #create an inputnode where you can set geometry
    geo_inputnode = ph.HInputNode(session, "Curve")

    #create a geocurve
    curve_geo = ph.HGeoCurve(
        vertices=np.array(
            [[-4.0, 0.0, 4.0],
             [-4.0, 0.0, -4.0],
             [4.0, 0.0, -4.0],
             [4.0, 0.0, 4.0]], dtype=np.float32),
        curve_knots=np.array(
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        curve_type=ph.CurveType.NURBS)

    #set this geocurve as geometry of inputnode
    geo_inputnode.set_geometry(curve_geo)


Marshall Curve Out
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/nurbs_curve.hda")
    asset_node = hda_asset.instantiate(node_name="Curve").cook()

    #get node's all display geo, print curveinfo and P
    all_geos = asset_node.get_display_geos()
    for geo in all_geos:
        print(geo.get_attrib_data(ph.AttributeOwner.POINT, "P"))
        if isinstance(geo, ph.HGeoCurve):
            print(geo.curve_info)

Marshall Mesh In
++++++++++++++++++++++++++++++++++++++++++++

Vertices should be in shape (num_vertices, 3)  
Faces should be in shape (num_faces, num_vertices_per_face)

.. code-block:: python

    import logging
    import numpy as np
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #create an inputnode where you can set geometry
    geo_inputnode = ph.HInputNode(session, "Cube")

    #create a geomesh
    cube_geo = ph.HGeoMesh(
        vertices=np.array(
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 1.0],
             [0.0, 1.0, 0.0],
             [0.0, 1.0, 1.0],
             [1.0, 0.0, 0.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 0.0],
             [1.0, 1.0, 1.0]], dtype=np.float32),
        faces=np.array(
            [[0, 2, 6, 4],
             [2, 3, 7, 6],
             [2, 0, 1, 3],
             [1, 5, 7, 3],
             [5, 4, 6, 7],
             [0, 4, 5, 1]], dtype=np.int32))

    #set this geomesh as geometry of inputnode
    geo_inputnode.set_geometry(cube_geo)

    #create a node whose input is inputnode
    ph.HNode(session, "Sop/subdivide", "Cube Subdivider").connect_node_input(geo_inputnode)

Marshall Mesh Out
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    # load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="TestObject").cook()
    asset_geos = asset_node.get_display_geos()

    for geo in asset_geos:
        print("Geo {0} has attribute {1}".format(geo, geo.get_attrib_names()))

    print(asset_geos[0].get_attrib_data(ph.AttributeOwner.POINT, "P"))

Marshall Heightfield In
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    import logging
    import numpy as np
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #create a heightfield input node, used to marshal in height and mask
    #it will create three node for height, mask and merge.
    height_input_node = ph.HHeightfieldInputNode(session, "height_input", 500, 500, 1)

    #a random height marshal into height node
    height_geo = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32)*100,
        "height")
    height_geo.commit_to_node(session, height_input_node.height_node.node_id)

    #a random mask marshal into mask node
    mask_geo = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32),
        "mask")
    mask_geo.commit_to_node(session, height_input_node.mask_node.node_id)

    #create a heightfield input volume node, usually used to marshal in custom mask
    heightvolume_input_node = ph.HHeightfieldInputVolumeNode(session, "water_mask", 500, 500, 1)

    #a random mask marshal in as water mask
    water_mask = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32)*0.5,
        "water_mask")
    water_mask.commit_to_node(session, heightvolume_input_node.node_id)

    #merge the watermask into heightfield input node
    #now the heightfield has three layer: height, mask and water_mask
    height_input_node.merge_node\
        .connect_node_input(heightvolume_input_node, input_index=2)\
        .cook()

Marshall Heightfield Out
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    import logging
    import pyhapi as ph

    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/heightfield_test.hda")
    asset_node = hda_asset.instantiate(node_name="HF").cook()

    #get node's all display geo, print volume's data shape and name
    all_geos = asset_node.get_display_geos()
    for geo in all_geos:
        if isinstance(geo, ph.HGeoHeightfield):
            print(geo.volume.shape)
            print(geo.volume_name)

Session Pool
--------------------------------------------

Process Multiple Tasks with HSessionPool
++++++++++++++++++++++++++++++++++++++++++++

You need to   

- add @ph.HSessionTask decorator to your task function  
- use session as first parameter of function  

.. code-block:: python

    import asyncio
    import pyhapi as ph

    @ph.HSessionTask
    async def session_task(session, index1, index2):
        print("execute {0} - {1}".format(index1, index2))
        hda_asset = ph.HAsset(session, "hda/save_cube.hda")
        asset_node = hda_asset.instantiate(node_name="cube")
        asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
        await asset_node.press_button_async("execute", status_report_interval=0.1)

    def main():
        """Main
        """
        logging.basicConfig(level=logging.INFO)

        session_pool = ph.HSessionManager.get_or_create_session_pool(3)
        
        for i in range(2):
            for j in range(2):
                session_pool.enqueue_task(session_task, i, j)
        
        # run all task by now and close
        session_pool.run_all_tasks()

    if __name__ == "__main__":
        main()

Use Task Producer Coroutine
++++++++++++++++++++++++++++++++++++++++++++

For tasks, you need to   

- add @ph.HSessionTask decorator to your task function  
- use HSession as first parameter of function  

.. code-block:: python

    import logging
    import asyncio
    import random
    import pyhapi as ph

    @ph.HSessionTask
    async def session_task(session : ph.HSession, index1, index2):
        print("execute {0} - {1}".format(index1, index2))
        hda_asset = ph.HAsset(session, "hda/save_cube.hda")
        asset_node = hda_asset.instantiate(node_name="cube")
        asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
        await asset_node.press_button_async("execute", status_report_interval=0.1)

    async def producer():
        while True:
            val1 = random.randint(1, 10)
            val2 = random.randint(10, 20)
            await asyncio.sleep(random.random())
            await ph.HSessionManager.get_or_create_session_pool().enqueue_task_async(session_task, val1, val2)

    def main():
        """Main
        """
        logging.basicConfig(level=logging.INFO)
        session_pool = ph.HSessionManager.get_or_create_session_pool()

        # run producer and consumer forever
        session_pool.run_on_task_producer(producer)

    if __name__ == "__main__":
        main()

Use Multiple Thread to Generate Tasks
++++++++++++++++++++++++++++++++++++++++++++

For tasks, you need to   

- add @ph.HSessionTask decorator to your task function  
- use HSession as first parameter of function  

.. code-block:: python

    import logging
    import asyncio
    import random
    import threading
    import time
    from concurrent.futures import ThreadPoolExecutor
    import pyhapi as ph

    @ph.HSessionTask
    async def session_task(session : ph.HSession, index1, index2):
        print("execute {0} - {1}".format(index1, index2))
        hda_asset = ph.HAsset(session, "hda/save_cube.hda")
        asset_node = hda_asset.instantiate(node_name="cube")
        asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
        await asset_node.press_button_async("execute", status_report_interval=0.1)

    def producer(n):
        while True:
            val1 = random.randint(1, 10)
            val2 = random.randint(10, 20)
            time.sleep(5*random.random())
            print("Task Start on {0}-{1}".format(n, threading.currentThread().getName()))
            try:
                fut = ph.HSessionManager.get_or_create_session_pool().enqueue_task(session_task, val1, val2)
                # block this producer thread
                while not fut.done():
                    time.sleep(0.5)
            except Exception as e:
                logging.exception(e)
            finally:
                print("Task Completed on {0}-{1}".format(n, threading.currentThread().getName()))

    def main():
        """Main
        """
        logging.basicConfig(level=logging.INFO)
        session_pool = ph.HSessionManager.get_or_create_session_pool()

        # run consumer on background thread forever
        session_pool.run_task_consumer_on_background()

        executor = ThreadPoolExecutor(max_workers=4)
        for i in range(0,4):
            executor.submit(producer, i)

    if __name__ == "__main__":
        main()

A Flask Houdini Server Demo
++++++++++++++++++++++++++++++++++++++++++++

A demo to run houdini on server and respond to restful api  

.. code-block:: python

    import os, time, datetime
    from flask import Flask, request, send_file
    import pyhapi as ph

    app = Flask(__name__)

    @ph.HSessionTask
    async def session_task(session : ph.HSession, filename, seed):
        hda_asset = ph.HAsset(session, "hda/save_cube.hda")
        asset_node = hda_asset.instantiate(node_name="cube")
        asset_node.set_param_value("filename", "{0}".format(filename))
        asset_node.set_param_value("seed", seed)
        await asset_node.press_button_async("execute", status_report_interval=0.1)

    @app.route('/sample', methods=['POST'])
    def sample():
        try:
            seed = request.json['seed']
            filename = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
            fut = ph.HSessionManager.get_or_create_session_pool().enqueue_task(session_task, filename, seed)
            while not fut.done():
                time.sleep(0.1)
            return send_file("{0}.obj".format(filename))
        except Exception as e:
            print(e)

    def main():
        session_pool = ph.HSessionManager.get_or_create_session_pool()
        session_pool.run_task_consumer_on_background()
        app.run(threaded=True, host='127.0.0.1')

    if __name__ == "__main__":
        main()