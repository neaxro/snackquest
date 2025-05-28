import axios from "axios";

const base_url = "http://localhost:5000"

export function getMachines(){
    const endpoint = `${base_url}/machines`;
    return axios.get(endpoint);
}

export function getInventory(machineName: string){
    const endpoint = `${base_url}/machines/${machineName}`;
    return axios.get(endpoint);
}