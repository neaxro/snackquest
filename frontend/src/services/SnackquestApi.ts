import axios from "axios";

const base_url = "http://localhost:5000"

export function getMachines(){
    const endpoint = `${base_url}/machines`;
    return axios.get(endpoint);
}
