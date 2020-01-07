import thunkMiddleware from "redux-thunk"
import { createStore, applyMiddleware } from "redux"
import { composeWithDevTools } from "redux-devtools-extension"
import rootReducer from "./reducers"
import { changeScreenSize } from "./dispatchers"
import { SCREEN_SIZES } from "./actions"


const composeEnhancers = composeWithDevTools

const store = createStore(
    rootReducer,
    composeEnhancers(
        applyMiddleware(
            thunkMiddleware
        )
    )
)

const mediaQuery = window.matchMedia('(max-width: 700px')

let sizeChangeHandler = (mq) => {
    if (mq.matches){
        changeScreenSize(
            SCREEN_SIZES.SMALL,
            store.dispatch
        )
    }
    else(
        changeScreenSize(
            SCREEN_SIZES.LARGE,
            store.dispatch
        )
    )
}

sizeChangeHandler(mediaQuery)

mediaQuery.addEventListener( sizeChangeHandler )

export default store