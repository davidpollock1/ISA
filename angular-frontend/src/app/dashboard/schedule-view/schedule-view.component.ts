import { Component } from '@angular/core';

@Component({
  selector: 'app-schedule-view',
  templateUrl: './schedule-view.component.html',
  styleUrl: './schedule-view.component.css'
})
export class ScheduleViewComponent {

  hours: string[] = Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2, '0')}:00`);
  sampleEvents: { title: string; startTime: string; endTime: string; }[];


  calculateTopMargin(startTime: string): number {
    const [hour, minute] = startTime.split(':').map(Number);
    return (hour * 60 + minute) / 60 * 4; // 4 pixels per hour
  }

  calculateEventHeight(startTime: string, endTime: string): number {
    const [startHour, startMinute] = startTime.split(':').map(Number);
    const [endHour, endMinute] = endTime.split(':').map(Number);
    const durationInMinutes = (endHour - startHour) * 60 + (endMinute - startMinute);
    return (durationInMinutes / 60) * 4; // 4 pixels per hour
  }

  next7Days: { date: Date; dayName: string; events: { name: string, top: number, height: number }[] }[] = [];

  month: string[];



  constructor() {

    this.sampleEvents = [
      { title: 'Meeting 1', startTime: '09:00', endTime: '10:30' },
      { title: 'Lunch', startTime: '12:00', endTime: '13:00' },
      { title: 'Meeting 2', startTime: '14:30', endTime: '16:00' },
      { title: 'Event 4', startTime: '18:00', endTime: '19:30' },
    ];

    const currentDate = new Date();

    this.month = [currentDate.toLocaleString('en-US', { month: 'long' })]

  }
}
