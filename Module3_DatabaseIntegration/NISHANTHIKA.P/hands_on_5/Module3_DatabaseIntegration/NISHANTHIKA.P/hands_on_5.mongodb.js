// ============================================================
// HANDS-ON 5: MongoDB — Document Modelling, CRUD & Aggregation
// Database: college_nosql | Collection: feedback
// ============================================================


// ── Task 1: Create Collection and Insert Documents ────────────────────────────

use college_nosql

db.createCollection("feedback")

// 62 AND 63: Insert 10+ feedback documents
db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching. Would recommend.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good course but assignments were very tough.",
    tags: ["challenging", "informative"],
    submitted_at: ISODate("2022-11-28T09:00:00Z"),
    attachments: [{ filename: "summary.pdf", size_kb: 180 }]
  },
  {
    student_id: 5,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 3,
    comments: "Average experience. More examples would help.",
    tags: ["average", "needs-improvement"],
    submitted_at: ISODate("2022-11-29T14:30:00Z"),
    attachments: []
  },
  {
    student_id: 1,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 4,
    comments: "Great practical exposure to databases.",
    tags: ["well-structured", "practical", "good-examples"],
    submitted_at: ISODate("2022-11-30T11:00:00Z"),
    attachments: [{ filename: "db_notes.pdf", size_kb: 310 }]
  },
  {
    student_id: 5,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 5,
    comments: "Best course this semester!",
    tags: ["excellent", "well-structured"],
    submitted_at: ISODate("2022-12-01T08:45:00Z")
    // No attachments field — demonstrating schema-less flexibility
  },
  {
    student_id: 3,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 2,
    comments: "Difficult to follow. Needed more visual aids.",
    tags: ["challenging", "needs-improvement"],
    submitted_at: ISODate("2021-11-25T16:00:00Z"),
    attachments: []
  },
  {
    student_id: 6,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 4,
    comments: "Solid fundamentals coverage.",
    tags: ["informative", "well-structured"],
    submitted_at: ISODate("2021-11-26T10:00:00Z"),
    attachments: [{ filename: "circuit_notes.pdf", size_kb: 120 }]
  },
  {
    student_id: 4,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 3,
    comments: "Decent course. Lab sessions were engaging.",
    tags: ["average", "practical"],
    submitted_at: ISODate("2023-11-20T13:00:00Z"),
    attachments: []
  },
  {
    student_id: 7,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 1,
    comments: "Not enough support for struggling students.",
    tags: ["needs-improvement", "challenging"],
    submitted_at: ISODate("2023-11-21T09:30:00Z"),
    attachments: []
  },
  {
    student_id: 8,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Very engaging and practical. Highly recommend!",
    tags: ["excellent", "challenging", "good-examples"],
    submitted_at: ISODate("2022-11-30T15:00:00Z"),
    attachments: [{ filename: "hw1.pdf", size_kb: 95 }]
  }
])

// Step 64: Verify inserts
db.feedback.countDocuments()  // should return 10+


// ── Task 2: CRUD Operations ───────────────────────────────────────────────────

// 65: READ — feedback with rating = 5
db.feedback.find({ rating: 5 })

// 66: READ — CS101 feedback where tags contains 'challenging'
db.feedback.find({
  course_code: "CS101",
  tags: "challenging"
})
// Using $elemMatch (for when matching multiple conditions on same element):
db.feedback.find({
  course_code: "CS101",
  tags: { $elemMatch: { $eq: "challenging" } }
})

// 67: READ — Projection: only student_id, course_code, rating (no _id)
db.feedback.find({}, {
  student_id: 1,
  course_code: 1,
  rating: 1,
  _id: 0
})

//  68: UPDATE — Add needs_review: true to all docs with rating < 3
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)

// 69: UPDATE — Push 'reviewed' tag to all needs_review docs
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
)

// 70: DELETE — Remove all feedback from semester '2021-EVEN'
db.feedback.deleteMany({ semester: "2021-EVEN" })


// ── Task 3: Aggregation Pipeline ─────────────────────────────────────────────

// 71: Pipeline — filter 2022-ODD, group by course, sort by avg rating
db.feedback.aggregate([
  // Stage 1: Filter to semester 2022-ODD
  { $match: { semester: "2022-ODD" } },

  // Stage 2: Group by course_code
  { $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
  }},

  // Stage 3: Sort by avg rating descending
  { $sort: { avg_rating: -1 } }
])

// 72: Extended pipeline — rename and round avg_rating
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  { $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
  }},
  { $sort: { avg_rating: -1 } },
  { $project: {
      course_code: "$_id",
      _id: 0,
      average_rating: { $round: ["$avg_rating", 1] },
      total_feedback: 1
  }}
])

// 73: Tag frequency leaderboard using $unwind
db.feedback.aggregate([
  // Deconstruct tags array — each tag becomes its own document
  { $unwind: "$tags" },

  // Count occurrences of each tag
  { $group: {
      _id: "$tags",
      count: { $sum: 1 }
  }},

  // Sort by count descending
  { $sort: { count: -1 } },

  // Rename _id to tag for clarity
  { $project: {
      tag: "$_id",
      count: 1,
      _id: 0
  }}
])

// 74: Add index on course_code and verify with explain
db.feedback.createIndex({ course_code: 1 })

// Verify: should show IXSCAN not COLLSCAN
db.feedback.find({ course_code: "CS101" }).explain("executionStats")
// winningPlan.inputStage.stage should be "IXSCAN" after index creation
