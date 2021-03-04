import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { BookModule } from './modules';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './modules/material/material.module';
@NgModule({
	declarations: [
		AppComponent,
	],
	exports: [
		MaterialModule,
	],
	imports: [
		BrowserModule.withServerTransition({ appId: 'jibot3' }),
		HttpClientModule,
		AppRoutingModule,
		BrowserAnimationsModule,
		MaterialModule,
		BookModule,
	],
	providers: [
	],
	bootstrap: [
		AppComponent
	]
})
export class AppModule {
	constructor () {	}
}
