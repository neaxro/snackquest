import axios from "axios";
import { Snack } from "../types/Snack";
import { TargetFunction } from "../types/TargetFunction";

const base_url = process.env.REACT_APP_BACKEND_URL;

export function getMachines(){
    const endpoint = `${base_url}/machines`;
    return axios.get(endpoint);
}

export function getInventory(machineName: string){
    const endpoint = `${base_url}/machines/${machineName}`;
    return axios.get(endpoint);
}

export function calculate(budget: number, target_function: TargetFunction, machineName: string, snacks: Snack[]){
    const endpoint = `${base_url}/solve?target_function=${target_function.param_name}&budget=${budget}`;
    return axios.post(
        endpoint,
        {
            items: snacks
        }
    );
}
