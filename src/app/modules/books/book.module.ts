import { APP_INITIALIZER, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
//import { ApiService } from '@app/modules/api/api.service';
import { BookService } from  './book.service';

@NgModule({
	declarations: [],
	exports: [],
	imports: [
		CommonModule
	],
	providers: [
		{
			provide:APP_INITIALIZER,
			deps: [BookService],
			multi: true,
			useFactory: (books:BookService) => () => books.init()
		},
	]
})
export class BookModule { }
