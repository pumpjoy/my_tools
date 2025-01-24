// Data for debugging
import 'models.dart';

final List<Note> notes = [
    Note(
    noteType: NoteType.simple,
    date: '2024-10-11',
    timeStart: '10:00:00',
    tag: ['Work', 'Good'],
    title: "**Test 1**",
    description: "**Test description**\n_test test test_",
    rating: 6
    ),

    Note(
    noteType: NoteType.simple,
    date: '2024-10-12',
    timeStart: '10:20:20',
    tag: ['Work', 'Good'],
    title: "**Test 2**",
    description: "**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_**Test 2 description**_test test test_",
    rating: 6
    ),

    Note(
    noteType: NoteType.autoTime,
    date: '2024-10-12',
    timeStart: '10:21:20',
    tag: ['Work', 'Good'],
    title: "**Test 3**",
    description: "**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_**Test 3 description**_test test test_",
    timeEnd: '10:31:02',
    durationPause: 32,
    rating: 6
    )
];