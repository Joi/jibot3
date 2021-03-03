import { APP_INITIALIZER, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './api.service';
@NgModule({
	// declarations: [],
	// imports: [
	// 	CommonModule
	// ],
	// providers: [
	// 	{
	// 		provide:APP_INITIALIZER,
	// 		deps: [ApiService],
	// 		multi: true,
	// 		useFactory: (api: ApiService) => () => api.init(),
	// 	},
	// ]
})
export class ApiModule { }
