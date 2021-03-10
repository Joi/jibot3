import {  NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BookService, BookServiceFactory } from './book.service';
import { FetcherService } from '@services/fetcher.service';
import { HttpClient } from '@angular/common/http';
@NgModule({
	declarations: [	],
	exports: [
        RouterModule
    ],
	imports: [
		CommonModule,
        RouterModule,
	],
	providers: [
        FetcherService,
		{
			provide: BookService,
			useFactory: BookServiceFactory,
			deps: [HttpClient, FetcherService]
		}
	]
})
export class BookModule { }
