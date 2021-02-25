import { TestBed } from '@angular/core/testing';

import { Sqlite3Service } from './sqlite3.service';

describe('Sqlite3Service', () => {
  let service: Sqlite3Service;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Sqlite3Service);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
