import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Option } from '@modules/options/option';
import { OptionsService } from '@modules/options/options.service';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.scss']
})
export class OptionsComponent implements OnInit, OnDestroy {
	public options: BehaviorSubject<Option[]> = new BehaviorSubject(null);
	private subscriber;
	constructor(
		private optionsService: OptionsService
	) {
		this.subscriber = this.optionsService.read().subscribe((options:Option[]) => this.options.next(options));
	}
	ngOnInit(): void {

	}
	ngOnDestroy(): void {
        this.subscriber.unsubscribe();
    }
}
