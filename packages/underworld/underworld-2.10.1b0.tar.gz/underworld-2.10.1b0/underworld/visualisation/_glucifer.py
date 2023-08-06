##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##
##                                                                                   ##
##  This file forms part of the Underworld geophysics modelling application.         ##
##                                                                                   ##
##  For full license and copyright information, please refer to the LICENSE.md file  ##
##  located at the project root, or contact the authors.                             ##
##                                                                                   ##
##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##


import underworld as uw
import errno
import underworld._stgermain as _stgermain
import os
import urllib
import time
import json
from base64 import b64encode
import underworld.libUnderworld as libUnderworld
import subprocess
from subprocess import Popen, PIPE, STDOUT
from . import objects
import sys
import os
from mpi4py import MPI

#Ignore SIGPIPE, required to prevent abort by petsc signal handler
from signal import signal, SIGPIPE, SIG_IGN
signal(SIGPIPE, SIG_IGN)

#Attempt to import lavavu module
try:
    import lavavu
    #Import into main too so can be accessed there
    #(necessary for interactive viewer/controls)
    import __main__
    __main__.lavavu = lavavu
except Exception as e:
    if uw.mpi.rank == 0:
        print(e,": module not found! disabling inline visualisation")
    from . import lavavu_null as lavavu

# lets create somewhere to dump data for this session
try:
    tmpdir = os.environ['TMPDIR']
except:
    tmpdir = "/tmp"

os.path.join(tmpdir,"glucifer")

try:
    os.makedirs(tmpdir)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

class Store(_stgermain.StgCompoundComponent):
    """  
    The Store class provides a database which records the drawing object data required 
    by a figures. It also provides associated routines for saving and reloading this 
    database to external files
    
    In addition to parameter specification below, see property docstrings for
    further information.

    Parameters
    ----------
    filename: str
        Filename to use for a disk database, default is to create a temporary database filename.
    split: bool
        Set to true to write a separate database file for each timestep visualised
    view: bool
        Set to true and pass filename if loading a saved database for re-visualisation
    compress: bool
        Set to true to enable database compression.

    Example
    -------
        
    Create a database:
    
    >>> import underworld.visualisation as vis
    >>> store = vis.Store()

    Optionally provide a filename so you don't need to call save later (no extension)
    
    >>> store = vis.Store('myvis')

    Pass to figures when creating them
    (Providing a name allows you to revisualise the figure from the name)
    
    >>> fig = vis.Figure(store, name="myfigure")
    
    When figures are rendered with show() or save(imgname), they are saved to storage
    If you don't need to render an image but still want to store the figure to view later,
    just call save() without a filename
    
    >>> fig.save()

    To create a timeseries of each figure you must increment the stores's internal
    'timestep' manually before calling the next save()/show().

    >>> store.step += 1
    >>> fig.save()
    
    Save the database (only necessary if no filename provided when created)
    
    >>> dbfile = store.save("myvis")

    """
    _objectsDict = { "_db":"lucDatabase" }
    _selfObjectName = "_db"
    viewer = None

    def __init__(self, filename=None, split=False, compress=True, **kwargs):

        self.step = 0
        if filename is None:
            filename = os.path.join(tmpdir,"tmpDB_"+self._db.name+".gldb")
        elif filename and not filename.lower().endswith('.gldb') and not filename.lower().endswith('.db'):
            filename += ".gldb"
        self.filename = filename
        self._objects = []
        #Don't split on timestep unless filename provided
        if not self.filename: split = False
        self._split = split
        self.compress = compress
        super(Store,self).__init__(**kwargs)

    def _add_to_stg_dict(self,componentDictionary):
        # lets build up component dictionary
        # append random string to provided name to ensure unique component names
        # call parents method
        super(Store,self)._add_to_stg_dict(componentDictionary)

        #Extension needs to added by lucDatabase when generating per timestep files
        filename = self.filename
        if filename:
            #Need base name, strip extensions if provided
            if filename.lower().endswith('.gldb'):
                filename = filename[0:-5]
            if filename.lower().endswith('.db'):
                filename = filename[0:-3]

        componentDictionary[self._db.name].update( {
                            "filename"          :filename,
                            "splitTransactions" :True,
                            "singleFile"        :not self._split,
                            "compressed"        :self.compress,
        } )

    def save(self,filename):
        """  
        Saves the database to the provided filename.
            
        Parameters
        ----------
        filename :str
            Filename to save file to.  May include an absolute or relative path.
        """
        if uw.mpi.rank == 0:
            if not isinstance(filename, str):
                raise TypeError("Provided parameter 'filename' must be of type 'str'. ")
            if not filename.lower().endswith('.gldb') and not filename.lower().endswith('.db'):
                filename += '.gldb'
            if filename != self.filename:
                libUnderworld.gLucifer.lucDatabase_BackupDbFile(self._db, filename)
            return filename

    def lvget(self):
        #Get existing viewer, if any, otherwuse create one
        if not self.viewer:
            self.lvrun()
        return self.viewer

    def lvrun(self, db=None, *args, **kwargs):
        #Create and execute a new viewer with passed args
        if not db:
            db = self._db.path
        if 'UW_VIS_PORT' in os.environ:
            kwargs['port'] = int(os.environ['UW_VIS_PORT'])
        self.viewer = lavavu.Viewer(cache=False, clearstep=True, database=db, timestep=self.step, *args, **kwargs)
        return self.viewer

    def _generate(self, figname, objects, props):
        #First merge object list with active
        starttime = MPI.Wtime()
        for obj in objects:
            #Add nested colourbar objects
            if obj._colourBar:
                objects.append(obj._colourBar)
                obj._colourBar.parent = obj #Save parent ref

            #Set default parent flag
            obj.parent = None

            #Add to stored object list if not present
            if obj not in self._objects:
                self._objects.append(obj)

        #Set default names on objects where omitted by user
        #Needs to be updated every time as indices may have changed
        for o in range(len(self._objects)):
            #Default name + idx if no user set name
            obj = self._objects[o]
            if not "name" in obj.properties:
                if obj.properties.get("colourbar"):
                   obj.properties["name"] = 'ColourBar_' + str(o)
                else:
                   obj.properties["name"] = obj._dr.type[3:] + '_' + str(o)

        #Set the write step
        self._db.timeStep = self.step

        #Delete all drawing objects in register
        for ii in range(self._db.drawingObjects.objects.count,0,-1):
            libUnderworld.StGermain._Stg_ObjectList_RemoveByIndex(self._db.drawingObjects.objects,ii-1, libUnderworld.StGermain.KEEP)

        #Add drawing objects to register and output any custom data on them
        for obj in self._objects:
            #Hide objects not in this figure (also check parent for colour bars)
            obj.properties["visible"] = bool(obj in objects or obj.parent and obj.parent in objects)

            #Ensure properties updated before object written to db
            libUnderworld.gLucifer.lucDrawingObject_SetProperties(obj._dr, obj._getProperties());
            if obj.colourMap:
                libUnderworld.gLucifer.lucColourMap_SetProperties(obj.colourMap._cm, obj.colourMap._getProperties());

            #Add the object to the drawing object register for the database
            libUnderworld.StGermain.Stg_ObjectList_Append(self._db.drawingObjects.objects,obj._cself)

        # go ahead and fill db
        libUnderworld.gLucifer._lucDatabase_Execute(self._db,None)

        #Write visualisation state as json data
        libUnderworld.gLucifer.lucDatabase_WriteState(self._db, figname, self._get_state(self._objects, props))

        #Output any custom geometry on objects
        if lavavu and uw.mpi.rank == 0 and any(x.geomType is not None for x in self._objects):
            lv = self.lvget() #Open/get the viewer
            for obj in self._objects:
                #Create/Transform geometry by object
                obj.render(lv)

        #Parallel custom render output
        if lavavu and any(hasattr(x, "parallel_render") for x in self._objects):
            #In case no external file has been written we need to create a temporary
            #database on root so the other procs can load it
            #Wait for temporary db to be written if not already using an external store
            comm = MPI.COMM_WORLD
            rank = uw.mpi.rank
            self.filename = comm.bcast(self.filename, root=0)
            #print uw.mpi.rank,self.filename
            #Open the viewer with db filename
            lv = self.lvrun(self.filename)
            #Loop through objects and run their parallel_render method if present
            for obj in self._objects:
                if hasattr(obj, "parallel_render"):
                    obj.parallel_render(lv, uw.mpi.rank)
            #Delete the viewer instance on non-root procs
            uw.mpi.barrier()
            if uw.mpi.rank > 0:
                lv = None
                self.viewer = None

#        if not lavavu.is_ipython():
#            endtime = MPI.Wtime()
#            print("Visualisation export took %10.2fs on proc %d" % (endtime-starttime, uw.mpi.rank))

    def _get_state(self, objects, props):
        #Get current state as string for export
        export = dict()
        #Global properties passed from figure
        export["properties"] = props
        #Objects passed from figure
        objlist = []
        for obj in objects:
            objlist.append(obj.properties)

        export["objects"] = objlist
        #TODO: ColourMap properties

        return json.dumps(export, indent=2)

    def empty(self):
        """    Empties all the cached drawing objects
        """
        self._objects = []

class Figure(dict):
    """  
    The Figure class provides a window within which drawing objects may be 
    rendered. It also provides associated routines for image generation
    and visualisation.
    
    In addition to parameter specification below, see property docstrings for
    further information.

    Parameters
    ----------
    store: underworld.visualisation.Store
        Database to collect visualisation data, this may be shared among figures
        to collect their data into a single file.
    name: str
        Name of this figure, optional, used for revisualisation of stored figures.
    resolution: tuple
        Image resolution provided as a tuple.
    boundingBox: tuple
        Tuple of coordinate tuples defining figure bounding box.
        For example ( (0.1,0.1), (0.9,0.9) )
    facecolour: str
        Background colour for figure.
    edgecolour: str
        Edge colour for figure.
    title: str
        Figure title.
    axis: bool
        Bool to determine if figure axis should be drawn.
    quality: unsigned
        Antialiasing oversampling quality. For a value of 2, the image will be
        rendered at twice the resolution, and then downsampled. Setting
        this to 1 disables antialiasing, values higher than 3 are not recommended..
    properties: str
        Further properties to set on the figure.
            
    Example
    -------
        
    Create a figure:
    
    >>> import underworld.visualisation as vis
    >>> fig = vis.Figure()

    We need a mesh
    
    >>> import underworld as uw
    >>> mesh = uw.mesh.FeMesh_Cartesian()

    Add drawing objects:
    
    >>> fig.append(vis.objects.Surface( mesh, 1.))

    Draw image. Note that if called from within a Jupyter notebook, image
    will be rendered inline. Otherwise, image will be saved to disk.
    
    >>> fig.show()
    
    Save the image
    
    >>> imgfile = fig.save("test_image")

    Clean up:
    
    >>> if imgfile: 
    ...     import os; 
    ...     os.remove( imgfile )

    """
    _viewerProc = None
    _id = 1

    def __init__(self, store=None, name=None, figsize=None, boundingBox=None, facecolour="white",
                 edgecolour="black", title="", axis=False, quality=3, *args, **kwargs):

        #Create a default database just for this figure if none provided
        if store and isinstance(store, Store):
            self.db = store
        else:
            self.db = Store()

        if name:
            if not isinstance(name,str):
                raise TypeError("'name' object passed in must be of python type 'str'")
        elif "name" in kwargs:
            name = kwargs["name"]
        else:
            name = "Figure_" + str(Figure._id)
            Figure._id += 1
        self.name = name

        if boundingBox and not isinstance(boundingBox,tuple):
            raise TypeError("'boundingBox' object passed in must be of type 'tuple'")
        if boundingBox and not isinstance(boundingBox[0],tuple):
            raise TypeError("'boundingBox[0]' object passed in must be of type 'tuple'")
        if boundingBox and not isinstance(boundingBox[1],tuple):
            raise TypeError("'boundingBox[1]' object passed in must be of type 'tuple'")

        if not isinstance(edgecolour,str):
            raise TypeError("'edgecolour' object passed in must be of python type 'str'")

        if not isinstance(axis,bool):
            raise TypeError("'axis' object passed in must be of python type 'bool'")

        if quality and not isinstance(quality,(int,float)):
            raise TypeError("'quality' object passed in must be of python type 'float' or 'int'")
        self["quality"]=quality

        #Setup default properties
        self.update({"resolution" : (640, 480), "title" : str(title), 
            "axis" : axis, "antialias" : True,
            "background" : facecolour, "margin" : 40, 
            "border" : (1 if edgecolour else 0), "bordercolour" : edgecolour, 
            "rulers" : False, "zoomstep" : 0})

        #    "size" : (0.75,0.02), 
        #    "margin" : 0.05})

        #User-defined props in kwargs
        self.update(kwargs)
        dict((k.lower(), v) for k, v in self.items())

        if boundingBox:
            #Add 3rd dimension if missing
            if len(boundingBox[0]) < 3 or len(boundingBox[1]) < 3:
                boundingBox = (tuple(list(boundingBox[0]) + [0]), tuple(list(boundingBox[1]) + [0]))
            self["min"] = boundingBox[0]
            self["max"] = boundingBox[1]

        #Legacy parameter
        if figsize and not isinstance(figsize,tuple):
            raise TypeError("'resolution' object passed in must be of python type 'tuple'")
        elif figsize:
            self["resolution"] = figsize
        
        self.draw = objects.Drawing()
        self._drawingObjects = []

        #Types of all Drawing derived classes
        def all_subclasses(cls):
            return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]

        #Object contructor shortcut methods
        #(allows constructing an object and adding to a figure directly from the figure object)
        for constr in all_subclasses(objects.Drawing):
            key = constr.__name__
            if key[0] == '_': continue; #Skip internal
            #Use a closure to define a new method to call constructor and add to objects
            def addmethod(constr):
                def method(*args, **kwargs):
                    obj = constr(*args, **kwargs)
                    self.append(obj)
                    return obj
                return method
            method = addmethod(constr)
            #Set docstring
            method.__doc__ = constr.__doc__
            self.__setattr__(key, method)

        super(Figure, self).__init__(*args)

    def _getProperties(self):
        #Convert properties to string
        return '\n'.join(['%s=%s' % (k,v) for k,v in self.items()]);

    def _setProperties(self, newProps):
        #Update the properties values (merge)
        #values of any existing keys are replaced
        self.update(newProps)

    @property
    def resolution(self):
        """    resolution (tuple(int,int)): size of window in pixels.
        """
        return self["resolution"]

    @property
    def facecolour(self):
        """    facecolour : colour of face background.
        """
        return self["background"]

    @property
    def edgecolour(self):
        """    edgecolour : colour of figure border.
        """
        return self["bordercolour"]

    @property
    def title(self):
        """    title : a title for the image.
        """
        return self["title"]

    @property
    def axis(self):
        """    axis : Axis enabled if true.
        """
        return self["axis"]

    @property
    def objects(self):
        """    objects : list of objects to be drawn within the figure.
        """
        return self._drawingObjects

    @property
    def properties(self):
        """    
        properties (dict): visual properties of viewport, passed to LavaVu to control 
        rendering output of figure.
        
        When using the property setter, new properties are set, overwriting any duplicate 
        keys but keeping existing values otherwise.
        """
        return self
    @properties.setter
    def properties(self, value):
        self._setProperties(value)

    def show(self, type="Image"):
        """    
        Shows the generated image inline within an ipython notebook.
        
        Parameters
        ----------
        type: str
            Type of visualisation to display ('Image' or 'WebGL').
        
        If IPython is installed, displays the result image or WebGL content inline

        If IPython is not installed, this method will call the default image/web 
        output routines to save the result with a default filename in the current directory

        """
        try:
            if type.lower() != "webgl" and lavavu.is_notebook():
                self._generate_DB()
                if uw.mpi.rank > 0:
                    return
                from IPython.display import display,Image,HTML
                #Return inline image result
                filename = self._generate_image()
                display(HTML("<img src='%s'>" % filename))
            else:
                #Fallback to export image or call viewer webgl export
                self.save(filename=self.name, type=type)
        except RuntimeError as e:
            print("Error creating image: ", e)
            pass
        except:
            raise

    @staticmethod
    def show_grid( *rows ):
        """
        Shows a set of Figure objects in a grid. Note that this method
        currently only supports rendering images within a Jupyter Notebook,
        and saving gridded images to a file is not currently supported.
        
        Parameters
        ----------
        rows: set of tuples
            Each provided tuple represents a row of Figures,
            and should only contain Figure class objects.

        Example
        -------

        Create a bunch of figures:

        >>> import underworld.visualisation as vis
        >>> fig1 = vis.Figure()
        >>> fig2 = vis.Figure()
        >>> fig3 = vis.Figure()
        >>> fig4 = vis.Figure()
        >>> fig5 = vis.Figure()
        >>> fig6 = vis.Figure()

        We need a mesh

        >>> import underworld as uw
        >>> mesh = uw.mesh.FeMesh_Cartesian()

        Add drawing objects as usual:
        
        >>> r = uw.function.input()
        >>> fig1.append(vis.objects.Surface( mesh, 1.))
        >>> fig2.append(vis.objects.Mesh( mesh ))
        >>> fig3.append(vis.objects.Mesh( mesh, nodeNumbers=True ))
        >>> fig4.append(vis.objects.Surface( mesh, r[0]))
        >>> fig5.append(vis.objects.Surface( mesh, r[1]))
        >>> fig6.append(vis.objects.VectorArrows( mesh, r ))

        Draw images in a grid. Note that in a Jupyter notebook,
        this will render the image within the notebook, though it will
        not be rendered in this example. Also note that `show_grid()`
        is a static method, and so we call it directly as below (instead
        of as a method on a `Figure` instance).
        
        >>> vis.Figure.show_grid( (fig1,fig2,fig3),
        ...                            (fig4,fig5,fig6)  )
        <IPython.core.display.HTML object>
        
        The above should generate a 2x3 (row x col) grid. For a 3x2 grid
        we would instead call:
        
        >>> vis.Figure.show_grid( (fig1,fig2),
        ...                            (fig3,fig4),
        ...                            (fig5,fig6)  )
        <IPython.core.display.HTML object>

        """
        try:
            from IPython.display import HTML, display
        except:
            return
        htmlstr ="""
            <style>
            table,td,tr,th {border:none!important}
            </style>
            """
        htmlstr = "<table  style=\" border:none!important; background-repeat:no-repeat; width:900px;margin:0;\">"
        
        for row in rows:
            if not isinstance( row, (list,tuple) ):
                raise ValueError("You must provide a 'list' type object for each row.")
            htmlstr += "<tr>"
            for cell in row:
                if not isinstance( cell, Figure ):
                    raise ValueError("Only 'Figure' class objects should be provided.")
                cell._generate_DB()
                htmlstr += "<td>"
                htmlstr += "<img src='%s'>" % cell._generate_image()
                htmlstr += "</td>"
            htmlstr += "</tr>"
        htmlstr += "</table>"
        display(HTML(htmlstr))


    def save_image(self, filename="", size=(0,0)):
        # For back compatibility
        return self.save(filename, size)

    def save_database(self, filename, regen=True):
        if regen:
            self._generate_DB()
        return self.db.save(filename)

    def save(self, filename=None, size=(0,0), type="Image"):
        """  
        Saves the generated image to the provided filename or the figure to the database.
        
        Parameters
        ----------
        filename :str
            Filename to save file to.  May include an absolute or relative path.
        size (tuple(int,int)): size of image in pixels, defaults to original figsize setting
            If omitted, simply saves the figure data without generating an image
        type: str
            Type of visualisation to save ('Image' or 'WebGL').
            
        Returns
        -------
        filename: str
            The final filename (including extension) used to save the image will be returned. Note
            that only the root process will return this filename. All other processes will not return
            anything.
        """
        self._generate_DB()
        if filename is None or uw.mpi.rank > 0:
            return
        if not isinstance(filename, str):
            raise TypeError("Provided parameter 'filename' must be of type 'str'. ")
        if size and not isinstance(size,tuple):
            raise TypeError("'size' object passed in must be of python type 'tuple'")

        try:
            if type.lower() == "webgl":
                lv = self.db.lvrun()
                return lv.webgl(filename + '.html')
            else:
                return self._generate_image(filename, size)
        except RuntimeError as e:
            print("LavaVu error: ", e)
            import traceback
            traceback.print_exc()
            pass

    def _generate_DB(self):
        objects = self._drawingObjects[:]
        #Only add default object if used
        if len(self.draw.vertices) > 0:
            objects.append(self.draw)
        self.db._generate(self.name, objects, self)

    def _generate_image(self, filename="", size=(0,0)):
        if uw.mpi.rank > 0:
            return
        try:
            #Render with viewer
            lv = self.db.lvrun(quality=self["quality"])
            imagestr = lv.image(filename, resolution=size)
            #Return the generated filename
            return imagestr
        except RuntimeError as e:
            print("LavaVu error: ", e)
            import traceback
            traceback.print_exc()
            pass
        return ""

    def window(self, *args, **kwargs):
        """ Open an inline viewer.

        This returns a new LavaVu instance to display the figure
        and opens it as an interactive viewing window.
        """
        #Open a new viewer instance and display window
        if uw.mpi.rank == 0:
            v = self.viewer(new=True, *args, **kwargs)
            #Ensure correct figure selected
            v.figure(self.name)
            #Show the inline window,
            v.window()
            return v

    def viewer(self, new=False, *args, **kwargs):
        """ Return viewer instance.

        Parameters
        ----------
        new: boolean
            If True, a new viewer instance will always be returned
            Otherwise the existing instance will be used if available
        """
        #Open/get viewer instance
        if uw.mpi.rank == 0:
            #Generate db if doesn't exist
            if not self.db._db.path:
                self._generate_DB()
            #Get a viewer instance, if new requested always run a new one
            if new:
                return self.db.lvrun(*args, **kwargs)
            else:
                return self.db.lvget(*args, **kwargs)

    def send_command(self, cmd, retry=True):
        """ 
        Run command on an open viewer instance.
        
        Parameters
        ----------
        cmd: str
            Command to send to open viewer.
        """
        if uw.mpi.rank == 0:
            self.open_viewer()
            url = "http://localhost:9999/command=" + urllib2.quote(cmd)
            try:
                #print url
                response = urllib2.urlopen(url).read()
                #print response
            except:
                print("Send command '" + cmd + "' failed, no response")
                if retry:
                    #Wait a few seconds so server has time to start then try again
                    print("... retrying in 1s ...")
                    time.sleep(1)
                    self.send_command(cmd, False)
                else:
                    print("... failed, skipping ...")
                    pass
    
    def append(self,drawingObject):
        """
        Add a drawing object to the figure. 
        
        Parameters
        ----------
        drawingObject: visualisation.objects.Drawing
            The drawing object to add to the figure
                
        
        """
        if not isinstance(drawingObject, objects.Drawing):
            raise TypeError("Object your are trying to add to figure does not appear to be of type 'Drawing'.")

        self._drawingObjects.append( drawingObject )

    @property
    def step(self):
        """    
        step (int): current timestep
        """
        return self.db.step

    @step.setter
    def step(self, value):
        #Sets new step on db
        self.db.step = value

class Viewer(lavavu.Viewer):
    """  
    The Viewer class provides an interface to load stored figures and revisualise them
    This is a wrapper of the LavaVu Viewer object
    
    In addition to parameter specification below, see property docstrings and 
    lavavu.Viewer help for further information.

    Parameters
    ----------
    filename: str
        Filename of database used to previously store the visualisation figures
            
    Example
    -------

    Create database to use
    
    >>> import underworld.visualisation as vis
    >>> store = vis.Store('myvis')
    >>> fig = vis.Figure(store, name="myfigure")
    >>> import underworld as uw
    >>> mesh = uw.mesh.FeMesh_Cartesian()
    >>> fig.append(vis.objects.Mesh(mesh))
    >>> fig.save()

    Now reopen database:
    
    >>> viewer = vis.Viewer('myvis')

    Iterate over the figures, print their names
    
    >>> for name in viewer.figures:
    ...     print(name)
    myfigure
    
    Get a figure by name and display
    (A chosen name can be provided when creating the figures to make this easier)
    
    >>> viewer.figure("myfig")
    >>> viewer.show()

    Display all figures at each timestep
    
    >>> for step in viewer.steps:
    ...    viewer.step = step
    ...    for name in viewer.figures:
    ...        viewer.figure(name)
    ...        viewer.show()

    """

    _index = 0

    def __init__(self, filename, *args, **kwargs):
        self._step = 0

        if not isinstance(filename,str):
            raise TypeError("'filename' object passed in must be of python type 'str'")
        if filename and not filename.lower().endswith('.gldb') and not filename.lower().endswith('.db'):
            filename += ".gldb"

        self.filename = filename

        if 'UW_VIS_PORT' in os.environ:
            kwargs['port'] = int(os.environ['UW_VIS_PORT'])

        super(Viewer, self).__init__(database=filename, *args, **kwargs)

    def show(self):
        self.display()

    def showall(self):
        for fig in self.figures:
            self.figure(fig)
            self.display()

