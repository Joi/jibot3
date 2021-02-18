import { TestBed } from '@angular/core/testing';

import { JibotService } from './jibot.service';

describe('JibotService', () => {
  let service: JibotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JibotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
