class Note {
  Note({
    required this.noteType,
    required this.date,
    this.timeStart,
    this.tag = const [],
    this.title,
    this.description,
    this.durationPause,
    this.timeEnd,
    this.rating
  });
  
  final NoteType noteType;
  final String date;
  final String? timeStart;
  final List<String>? tag;
  final String? title;
  final String? description;
  final int? durationPause; // in seconds
  final String? timeEnd;
  final int? rating; 

}

enum NoteType {
  simple, 
  autoTime, 
  manualTime,
}