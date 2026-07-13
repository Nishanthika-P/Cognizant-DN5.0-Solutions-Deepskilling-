import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

// Services in Angular are singletons by default (providedIn: 'root') —
// one instance is shared across the whole app.
@Injectable({ providedIn: 'root' })
export class CourseService {
  private readonly apiUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=5';

  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map((posts) =>
        posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS${100 + index}`,
          credits: 3 + (index % 2),
          grade: '-',
        }))
      )
    );
  }
}
