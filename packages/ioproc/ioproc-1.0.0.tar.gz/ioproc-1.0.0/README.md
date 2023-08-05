# The ioProc workflow manager
ioProc is light-weight workflow manager for Python ensuring robust, scalable and reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.

## default actions provided by ioProc

### readExcel
This function is used to parse Excel files and storing it in the Data manager.
    
    @action('general')
    def readExcel(dmgr, config, params):
        '''
        reads excel files
    
        :param fieldName: the name of the datamanager field to store the data to
        :param param1: the data to be stored in the data manager
        :param param2: currently unused
        '''
        with dmgr.overwrite:
            dmgr[params['fieldName']] = params['param1']
            dmgr['data3'] = [1, 2, 3]

### checkpoint
Checkpoints save the current state and content of the data manger to disk in HDF5 format. The workflow can be resumed at any time from previously created checkpoints.

    @action('general')
    def checkpoint(dmgr, config, params):
        '''
        creates a checkpoint file in the current working directory with name
        Cache_TAG while TAG is supplied by the action config.
    
        :param tag: the tag for this checkpoint, this can never be "start"
        '''
        assert params['tag'] != 'start', 'checkpoints can not be named start'
        dmgr.toCache(params['tag'])
        mainlogger.info('set checkpoint "{}"'.format(params['tag']))

### printData
This action prints all data stored in the data manager to the console. It can therefore be used for conveniently debugging a workflow.

    @action('general')
    def printData(dmgr, config, params):
        '''
        simple debugging printing function. Prints all data in the data manager.
    
        Does not have any parameters.
        '''
        for k, v in dmgr.items():
            mainlogger.info(k+' = \n'+str(v))