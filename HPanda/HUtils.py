# HPanda
# Utility functions

# ###CopyRight notice####


# ###################

#imports

from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode


def modelToConvex(model):
    """

    :type model: panda3d.core.NodePath
    :return: tuple(panda3d.bullet.BulletConvexHull,transform)
    """
    geomnodes = model.findAllMatches('**/+GeomNode')
    transform = model.getTransform()
    gn = geomnodes.getPath(0).node()
    geom = gn.getGeom(0)
    shape = BulletConvexHullShape()
    shape.addGeom(geom)
    return shape, transform


def modelToShape(model, dynamic=False):
    """

    :type model: panda3d.core.NodePath
    :type dynamic: bool
    :return: tuple(panda3d.bullet.BulletTriangleMeshShape, transform)
    """
    geomnodes = model.findAllMatches('**/+GeomNode')
    transform = model.getTransform()
    gn = geomnodes.getPath(0).node()
    geom = gn.getGeom(0)
    mesh = BulletTriangleMesh()
    mesh.addGeom(geom)
    shape = BulletTriangleMeshShape(mesh, dynamic)
    return shape, transform


def modelToRigid(model, parent, name="Static"):
    """

    :type model: panda3d.core.NodePath
    :type parent: panda3d.core.NodePath
    :type name: str
    :return: tuple(panda3d.core.NodePath,panda3d.bullet.BulletRigidBodyNode)
    """
    rtuple = modelToShape(model)
    staticRigid = BulletRigidBodyNode(name)
    staticRigid.addShape(rtuple[0], rtuple[1])
    np = parent.attachNewNode(staticRigid)
    return np, staticRigid


def modelToShape2(model):
    """

    :type model: str
    :return: panda3d.bullet.BulletTriangleMeshShape
    """
    np = loader.loadModel(model)  #####componer luego
    mesh = BulletTriangleMesh()
    for geomNP in np.findAllMatches('**/+GeomNode'):
        geomNode = geomNP.node()
        ts = geomNP.getTransform(np)
        for geom in geomNode.getGeoms():
            mesh.addGeom(geom, ts)
    shape = BulletTriangleMeshShape(mesh, False)
    return shape


def blenderToPandaCameraRot(x, y, z):
    """

    :type x: float
    :type y: float
    :type z: float
    :return: tuple(float,float,float)
    """
    return tuple((z, -(90 - x), y))


def between(x, a, b):
    if b > x > a:
        return True
    else:
        return False


def sing(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0