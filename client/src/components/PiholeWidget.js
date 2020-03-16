import React, { useEffect } from 'react';
import axios from 'axios';


export default function PiholeWidget() {

  // useEffect(() => {
  //   Promise.all([
  //     axios.get('http://192.168.1.155/admin/api.php')
      
  //   ]).then((all) => {
  //     console.log(all)
  //   })
  //     .catch((e) => { });
  // }, []);

  // useEffect(() => {



  //   fetch('http://192.168.1.155/admin/api.php', {
  //     method: 'GET', // *GET, POST, PUT, DELETE, etc.
  //     mode: 'no-cors', // no-cors, *cors, same-origin
  //     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
  //     // credentials: 'same-origin', // include, *same-origin, omit
  //     headers: {
  //       'Content-Type': 'application/json'
  //       // 'Content-Type': 'application/x-www-form-urlencoded',
  //     },
  //     // redirect: 'follow', // manual, *follow, error
  //     // referrerPolicy: 'no-referrer', // no-referrer, *client
  //     // body: JSON.stringify(data) // body data type must match "Content-Type" header
  //   })
  //     .then((res) => {
  //       console.log(res)
  //     })
  // }, [])

  return(
    <p></p>
  )
}