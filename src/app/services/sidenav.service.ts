import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SidenavService {
	public toggle: BehaviorSubject<boolean> = new BehaviorSubject(null);
  	constructor() { }
}
