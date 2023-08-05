"""
Base classes for performing 'tasks' of simulations

Base classes for performing 'tasks' of simulations. 
"""


import logging




logger = logging.getLogger(__name__)








class Observable(object):

    """Class corresponding to an 'observable' - something to be measured
    during a task

    Class corresponding to an 'observable' - something to be measured
    during a task

    Attributes
    ----------
    descriptor : tuple
        Tuple of variables (normally strings and integers) which characterise
        the observable. For example the observable energy could have `descriptor`
        as ( "energy", ), and the number of molecules belonging to the 2nd
        molecular species in the system could be ( "nmols", 2 )

    """

    def __init__(self, descriptor):

        self.descriptor = descriptor




    def __str__(self):

        """Return a readable string representation of an Observable object

        Return a readable string representation of an Observable object, namely,
        string representations of each element in the `descriptor` all joined 
        together by underscores. This whitespace-free string representation is
        useful because the string representation of an Observable will be used
        in constructing names of output files pertaining to that observable,
        for which whitespace is undesirable
        """

        tojoin = []
        for i in range(0,len(self.descriptor)):
            tojoin.append( str(self.descriptor[i]) )
        return "_".join(  tuple(tojoin) )




    # Required for Observable objects to be keys in dictionaries
    def __hash__(self):

        return hash( self.descriptor )




    # Required for Observable objects to be keys in dictionaries
    def __eq__(self, other):

        return self.descriptor == other.descriptor








class TaskInterface(object):

    """Base class for interfacing with specific simulation codes

    Base class for interfacing with specific simulation codes. A Task object
    must be initialised using a TaskInterface object: the latter tells the former
    how to perform various tasks pertaining to the specific molecular 
    simulation code in question. A subclass of TaskInterface should be created
    for the particular simulation code one wishes to use with the Task class,
    where the functions in this class are overwritten by functions which correspond
    to the simulation code in question

    """

    def __init__(self):

        # Don't through a NotImplementedError - simple testing is easier
        # if we can create these objects
        pass




    def __str__(self):

        """Return a readable string representation of a TaskInterface object

        Return a readable string representation of a TaskInterface object. This
        is simply the class' name
        """

        return self.__class__.__name__




    def copy_input_files(self, fromdir, todir):

        """Copy simulation input files between directories

        Copy simulation input files between directories

        Parameters
        ----------
        fromdir : str
            The directory containing the input files
        todir : str
            The target directory for the input files
       
        """

        raise NotImplementedError




    def run_sim(self, simdir):

        """Run a simulation

        Run a simulation in a specified directory

        Parameters
        ----------
        simdir : str
            The directory in which the simulation is to be executed
       
        """

        raise NotImplementedError


    

    def resume_sim(self, oldsimdir, simdir):

        """Resume a simulation from a checkpointed state

        Resume a simulation whose checkpointed state is located in the
        directory `oldsimdir`, and run the resumed/new simulation in
        the directory `simdir`

        Parameters
        ----------
        oldsimdir : str
            The directory in which the files from the 'old' simulation
            to be resumed reside
        simdir : str
            The directory in which the new/resumed simulation is to be
            executed

        """

        raise NotImplementedError




    def extract_data(self, observable, simdir):

        """Extract simulation data corresponding to a specified observable
        
        Extract data corresponding to a specified observable from output
        files generated by a simulation in the directory `simdir`

        Parameters
        ----------
        observable : Observable
            The observable to extract
        simdir : str
            The directory containing the output files to extract data from

        Returns
        -------
        array
            An array containing one or more values corresponding to 
            `observable`.
       
        Raises
        ------
        ValueError
            If `observable` is not recognised or supported by this function

        Notes
        -----
        * Normally the returned array would be a time series, e.g., if
          `observable` is an energy then the returned array would contain
          the observed values of the energy vs. simulation time obtained
          from the simulation. However the array need not necessarily be
          a time series. E.g. it could be a radial distribution function.
          The nature of the values will depend on `observable`

        """

        raise NotImplementedError




    def amend_input_parameter(self, dir, parameter, value):
        
        """Amend a specific simulation input parameter

        Amend the parameter `parameter` in the input files in `dir` to 
        take the value `value`

        Parameters
        ----------
        dir : str
            The directory containing the input files
        parameter : str
            Name of parameter to amend
        value : str
            New value of the parameter

        Raises
        ------
        ValueError
            If `parameter` is not recognised or supported by this function

        """

        raise NotImplementedError








class Task(object):

    """Base class corresponding to a simulation task

    Base class corresponding to a simulation task.

    Attributes
    ----------
    interface : task.TaskInterface
        TaskInterface object corresponding to the molecular simulation code to
        be used

    """

    def __init__(self, task_interface):

        self.interface = task_interface



    
    def run(self):

        """Perform the task

        Perform the task
        """

        raise NotImplementedError













