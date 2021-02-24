import { Inject, Injectable } from '@angular/core';
@Injectable({
	providedIn: 'root'
})
export class LoggerService {
	public log = (message:any) => console.log(message);
	public warn = (message:any) => console.warn(message);
	public error = (message:any) => console.error(message);
	public init() {
		console.log(`Initializing ${this.constructor.name}...`);
	}
	public init_done() {
		console.log(`Initializing ${this.constructor.name} COMPLETE.`);
	}
}
