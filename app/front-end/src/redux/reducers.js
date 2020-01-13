import { combineReducers } from "redux"
import { TYPES, SCREEN_SIZES } from "./actions"


const surveys = function(state = {
    isFetching: false,
    fetchFailed: false,
    data: []
}, action){
    switch(action.type){
        case TYPES.REQUEST_SURVEYS:
            return {
                ...state,
                isFetching: true 
            }
        case TYPES.RECIEVE_SURVEYS_FAILED:
            return {
                ...state,
                isFetching: false,
                fetchFailed: true,
                failedAt: action.failedAt,
                failedBecause: action.failedBecause,
                httpStatus: action.httpStatus
            }
        case TYPES.RECIEVE_SURVEYS:
            let copiedState = {
                ...state,
                isFetching: false
            }
            
            delete copiedState.httpStatus
            delete copiedState.failedAt
            delete copiedState.failedBecause

            if (copiedState.data.length === 0 ){
                copiedState.data = action.surveys
            }
            else if(action.surveys.length > 0){
               let uuid_list_old = copiedState.data.map(
                   (value) => {
                       return value.uuid
                   }
                )
               
                let uuid_list_new = action.surveys.map(
                    (value) => {
                        return value.uuid
                    }
                )

                let indexOverlap = uuid_list_old.indexOf(uuid_list_new[0])

                if (indexOverlap === -1) {
                    copiedState.data = [...copiedState.data, ...action.surveys]
                }
                else {
                    copiedState.data = [...copiedState.data, ...action.surveys.slice(indexOverlap + 1)]
                }
            }

            return copiedState
        
        default:
            return state
    }

}

const screenSize = function(state = SCREEN_SIZES.SMALL, action) {
    switch( action.type ) {
        case TYPES.SCREEN_RESIZE:
            return action.screenSize
        default:
            return state
    }
}

const rootReducer = combineReducers(
    {
      surveys,
      screenSize 
    }
)

export default rootReducer