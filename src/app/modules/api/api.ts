import { HttpHeaders, HttpParams } from "@angular/common/http";
export interface Api {
	name: 		string,
	url:		URL,
	headers?:	HttpHeaders,
	params?:	HttpParams,
}
