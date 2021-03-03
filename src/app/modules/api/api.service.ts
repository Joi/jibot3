import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LoggerService } from '@services/logger.service';
@Injectable({
	providedIn: 'root'
})
export class ApiService {
	constructor(
		private http: HttpClient,
	) {	}
	private create() { }
	private read() { }
	private update() { }
	private destroy() {	}
}
