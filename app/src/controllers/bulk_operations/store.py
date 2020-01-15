from functools import wraps
from src.utils.errors.custom_errors import ActionAlreadyExistsInStore, HTTPMethodInvalid
from http_methods import GET, PATCH, PUT, POST, DELETE

methods = [ GET, PUT, POST, PATCH, DELETE ]

class ActionStore:
    def __init__(self):
        self.store = {}
    
    def resgister_action(self, action, action_description, http_methods_to_access):
        """
        used to register actions to the store

        Parameters
        ----------

        action: str
            the action name
        action_description:
            the description of the action
        """
        if not isinstance(action, str):
            raise TypeError("acton must be of type string recieved %s" % type(action).__name__)

        if not isinstance(action_description, str):
            raise TypeError("action_description must be of type string recieved %s" % type(action_description).__name__)
        
        if isinstance(http_methods_to_access, str):
            if http_methods_to_access not in methods:
                raise HTTPMethodInvalid(
                    f"HTTP method {http_methods_to_access} for action {action} is invalid must be one of " + " ".join(methods) 
                )
        elif isinstance(http_methods_to_access, list):
            for method in http_methods_to_access:
                if method not in methods:
                    raise HTTPMethodInvalid(
                        f"HTTP method {http_methods_to_access} for action {action} is invalid must be one of " + " ".join(methods) 
                    )
        else:
            raise TypeError(
                "http_methods_to_access must be of type string or list, recieved %s " % type(http_methods_to_access).__name__
            )

        if self.store.get(action) is not None:
            raise ActionAlreadyExistsInStore(
                f"Action {action} has been previously defined in store"
            )

        def action_register(view_func):

            # adding action to store 
            self.store[action] = {
                "description" : action_description,
                "httpMethods": http_methods_to_access,
                "action": view_func
            }

            @wraps(view_func)
            def action_wrapper(**kwargs):
                # wrapping action execution in try catch to catch errors 
                try:
                    view_func(**kwargs)
                # TODO: What should be done in the case of an exception
                except Exception as e:
                    pass
            
            return action_wrapper
        return action_register





        

