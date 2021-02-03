import { TestBed, async } from '@angular/core/testing';
import { AppComponent } from './app.component';
	describe('AppComponent', () => {
	beforeEach(async(() => {
		TestBed.configureTestingModule({
		declarations: [
			AppComponent
		],
		}).compileComponents();
	}));

	it('should create the app', () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.debugElement.componentInstance;
		expect(app).toBeTruthy();
	});

	it(`should have as title 'jibot3'`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.debugElement.componentInstance;
		expect(app.title).toEqual('jibot3');
	});
});
