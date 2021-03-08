import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatabaseService } from '@app/services/database.service';

@Injectable({
	providedIn: 'root'
})
export class OptionsService extends DatabaseService {}

export function OptionsServiceFactory(http:HttpClient) {
	return new OptionsService(http, "options");
}