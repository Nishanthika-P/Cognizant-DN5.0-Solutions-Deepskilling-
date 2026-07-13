import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseCardComponent } from '../course-card/course-card.component';
import { CourseService, Course } from '../../services/course.service';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  templateUrl: './course-list.component.html',
  styleUrl: './course-list.component.css',
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  searchTerm = '';
  loading = true;
  error: string | null = null;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (courses) => {
        this.courses = courses;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load courses. Please try again later.';
        this.loading = false;
      },
    });
  }

  get filteredCourses(): Course[] {
    const term = this.searchTerm.toLowerCase();
    return this.courses.filter((course) =>
      course.name.toLowerCase().includes(term)
    );
  }

  trackById(_index: number, course: Course): number {
    return course.id;
  }
}
