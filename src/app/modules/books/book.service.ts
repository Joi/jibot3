import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DatabaseService } from '@app/services/database.service';

@Injectable({
  providedIn: 'root'
})
export class BookService extends DatabaseService {}

export function BookServiceFactory(http:HttpClient) {
	return new BookService(http, "books");
}