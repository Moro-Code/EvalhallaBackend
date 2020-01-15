


class ClientError(Exception):
    pass

class NoResultsFoundInDatabase(ClientError):
    pass


class InternalError(Exception):
    pass 

class DatabaseCommitFailed(InternalError):
    pass



class ActionAlreadyExistsInStore(ValueError):
    pass

class HTTPMethodInvalid(ValueError):
    pass