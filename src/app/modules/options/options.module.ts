import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

import { OptionsService, OptionsServiceFactory } from './options.service';

@NgModule({
	declarations: [	],
	exports: [	],
	imports: [CommonModule],
	providers: [
		{
			provide: OptionsService,
			useFactory: OptionsServiceFactory,
			deps: [HttpClient]
		}
	]
})
export class OptionsModule { }
