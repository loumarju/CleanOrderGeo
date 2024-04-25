import maya.cmds as cmds

objects = cmds.ls(selection = True)
Nombre = "NombreProp"
PrefijoGeo = "pro_"
PrefijoColeccMain = "Pr-" 

# Crea una nueva ventana
window = cmds.window(title="SetUp Rigging", widthHeight=(250, 100))

# Crea un layout para los controles
cmds.columnLayout(adjustableColumn=True)

# Crea un botón para limpiar la geometría
cmds.button(label="Clean Geometry", command='clean_geometry()')

# Crea un botón para ordenar la geometría
cmds.button(label="Order Collections", command='order_geometry()')

# Muestra la ventana
cmds.showWindow(window)

# Define la función para limpiar la geometría
def clean_geometry():
    # Aquí va el código para limpiar la geometría

    #Limpiar transformaciones y keys

    for obj in objects:
        
        attributes = ['translateX', 'translateY', 'translateZ', 
                    'rotateX', 'rotateY', 'rotateZ', 
                    'scaleX', 'scaleY', 'scaleZ', 'visibility']

        for attr in attributes:
            # Obtén las conexiones para cada atributo
            connections = cmds.listConnections(obj + '.' + attr, s=True, d=False)

            if connections:
                # Desconecta cada conexión
                for conn in connections:
                    cmds.disconnectAttr(conn + '.output', obj + '.' + attr)

        cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)


# Define la función para ordenar la geometría
def order_geometry():
    # Aquí va el código para ordenar la geometría

    #Obtenemos la geometría seleccionada
    selected_geometry = cmds.ls(selection=True)[0]

    #Crea el grupo principal
    main_group = cmds.group(em=True, name=PrefijoColeccMain + selected_geometry)

    # Crea los grupos secundarios
    controls_group = cmds.group(em=True, name=PrefijoGeo + 'controls_grp')
    geo_group = cmds.group(em=True, name=PrefijoGeo + 'geo_grp')
    stuff_group = cmds.group(em=True, name=PrefijoGeo + 'stuff_grp')

    # Crea el grupo dentro de stuff_group
    skeleton_group = cmds.group(em=True, name=PrefijoGeo + 'skeleton_grp')

    # Añade los grupos secundarios al grupo principal
    cmds.parent(controls_group, main_group)
    cmds.parent(geo_group, main_group)
    cmds.parent(stuff_group, main_group)

    # Añade skeleton_group a stuff_group
    cmds.parent(skeleton_group, stuff_group)

    # Añade la geometría seleccionada a geo_group
    cmds.parent(selected_geometry, geo_group)

    # Mueve la geometría fuera de main_group
    cmds.parent(selected_geometry, world=True)

    # Crea la capa de rig
    rig_layer = cmds.createDisplayLayer(name='Rig', number=1, noRecurse=True)

    # Añade el grupo de controles a la capa
    cmds.editDisplayLayerMembers(rig_layer, skeleton_group)

    # Crea la capa de controles
    controls_layer = cmds.createDisplayLayer(name='Controls', number=1, noRecurse=True)

    # Añade el grupo de controles a la capa
    cmds.editDisplayLayerMembers(controls_layer, controls_group)

    # Mueve la geometría de nuevo a geo_group
    cmds.parent(selected_geometry, geo_group)

    #Crea las layers de Geometría y bloqueala
    selected_geometry = cmds.ls(selection=True)[0]
    GeoLayer = cmds.createDisplayLayer(name = 'Geo', number=1, noRecurse=True)
    cmds.editDisplayLayerMembers(GeoLayer, selected_geometry)
    cmds.setAttr(GeoLayer + '.displayType', 2)

