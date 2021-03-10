import { TestBed } from '@angular/core/testing';

import { BoltService } from './bolt.service';

describe('BoltService', () => {
  let service: BoltService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BoltService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
