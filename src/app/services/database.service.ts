import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
	providedIn: 'root'
})
export class DatabaseService {
	private apiBase:string = "http://localhost:3000";
	private apiRoute: string;
	constructor(
		private http: HttpClient,
		@Inject('entityName') private entityName: string
	) {
		console.log(this.entityName);
		this.apiRoute = `${this.apiBase}/${this.entityName}`;
	}
	private request(method: string, url: string, data?: any):Observable<any> {
		return this.http.request(method, url, {
			body: data,
			responseType: 'json',
			observe: 'body',
		});
	}
	public create	= (entity:any)	=> this.request('post', this.apiRoute, entity)
	public read		= (entity?:any)	=> this.request('get', (entity) ? `${this.apiRoute}/${entity.id}` : this.apiRoute);
	public update	= (entity:any)	=> this.request('post', `${this.apiRoute}/${entity.id}`, entity);
	public delete	= (entity:any)	=> this.request('delete', `${this.apiRoute}/${entity.id}`);
}