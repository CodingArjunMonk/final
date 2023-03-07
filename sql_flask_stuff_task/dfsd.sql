select students. name, city, courses.courseName, courseDetails from courses
INNER JOIN courseDetails ON courses. courseName=courseDetails.courseName
Inner JOIN students ON students.name = courses. studentName
where courses.courseName="BTEC Games Design"