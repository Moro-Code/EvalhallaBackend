import React from 'react';
import NavMenu from "./components/organisms/navigation/navMenu"
import Home from "./components/organisms/home/home"
import {
  Switch,
  Route
} from "react-router-dom"

function App() {
  const routes = [
    {
      linkText: "Home",
      link: "/",
      icon: "icon-survey-list"
    },
    {
      linkText: "Upload",
      link: "/upload",
      icon: "icon-upload"
    },
    {
      linkText: "Download",
      link: "/download",
      icon: "icon-download"
    }
  ]

  return (
    <div className="App">
      <NavMenu links = {routes}>   
      </NavMenu>
      <div id = "content">
        <Switch>
          <Route path = "/">
              <Home/>
          </Route>
        </Switch>
      </div>
    </div>
  );
}

export default App;
