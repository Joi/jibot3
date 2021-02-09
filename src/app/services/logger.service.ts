import { Injectable } from '@angular/core';

@Injectable({
	providedIn: 'root'
})
export class LoggerService {
	constructor() {	}
	public log = (message:any) => console.log(message);
	public warn = (message:any) => console.warn(message);
	public error = (message:any) => console.error(message);
}
