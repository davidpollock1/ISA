import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import flatpickr from 'flatpickr';

@Component({
    selector: 'app-date-picker',
    templateUrl: './date-picker.component.html',
    styleUrl: './date-picker.component.css',
    standalone: false
})

export class DatePickerComponent {

  @ViewChild('calendarInput') calendarInput!: ElementRef;
  date!: FormControl;

  ngAfterViewInit() {
    console.log('ngOnInit called');
    this.date = new FormControl();
    flatpickr(this.calendarInput.nativeElement, {
      // Set the 'open' option to true to keep the calendar always open
      inline: true,
      onChange: (selectedDates: Date[]) => {
        // Access the selected date from the array
        const selectedDate = selectedDates[0];
        console.log('Selected Date:', selectedDate);
      }
    });
  }
}