from .operations import READ, CREATE, UPDATE, DELETE
from src.utils.errors.messages import MISSING_PARAMETER_FOR_DATA_OPERATION
from src.database.db import get_db

def requires_params(operation, table, *args):
    # make sure all arguments are strings
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError("all arguments must be a string for this decorator")
    
    operations = [READ, UPDATE, CREATE, DELETE]

    if operation not in operations:
        raise ValueError(
            f"operation {operation} is not a valid CRUD operation"
        )

    def requires_param_wrapper(func):
        def check_if_correct_params_exist(self, **kwargs):
            non_present_params = []

            # we might potentially be mutating state so better to create a seperate copy and
            # alter this so as to prevent difficult to diagnose errors 
            func_kwargs = dict(kwargs)
    

            for arg in args:
                if arg not in func_kwargs and not hasattr(self, arg):
                    non_present_params.append(arg)
                elif hasattr(self, arg) and (getattr(self, arg) is not None):
                    func_kwargs[arg] = getattr(self, arg)

            if len(non_present_params) > 0:
                params_missing_str = ",".join(non_present_params)
                raise ValueError(
                    MISSING_PARAMETER_FOR_DATA_OPERATION.format(
                        operation = operation.lower(),
                        table = table,
                        parameters = params_missing_str
                    )
                )
            if not hasattr(self, "session"):
                self.session = get_db()
            return func(self, self.session, **func_kwargs)

        return check_if_correct_params_exist
    return requires_param_wrapper