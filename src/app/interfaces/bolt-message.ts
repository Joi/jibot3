import { BoltEvent } from './bolt-event';
export interface BoltMessage extends BoltEvent {
	regex?:	any;
}
