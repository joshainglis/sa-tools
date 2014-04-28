import 'dart:html';
import 'dart:math';
import 'package:intl/intl_browser.dart';
import 'package:intl/intl.dart';


Map<String, Map<String, Object>> disp;
TableElement ctable;
TableCellElement yr_cell;
TableCellElement t_cell;
TableRowElement current_row;
int age;
String sex;
double life;
double yr_total;
double lf_total;
InputElement toDoInput;
UListElement toDoList;
NumberFormat aud = new NumberFormat.currencyPattern("en_AU");

void main() {
  toDoInput = querySelector('#to-do-input');
  toDoList = querySelector('#to-do-list');
  toDoInput.onChange.listen(addToDoItem);
}

void addToDoItem(Event e) {
  var newToDo = new LIElement();
  newToDo.text = toDoInput.value;
  toDoInput.value = '';
  toDoList.children.add(newToDo);
}

void updateLifeTotalCell() {
  t_cell.text = aud.format(lf_total);
}

int getQty(String rowID) {
  TableCellElement current_cell = querySelector(rowID);
  String rid = rowID.substring(1, rowID.length - 4);
  int val;
  try {
    val = int.parse(current_cell.text);
  } on FormatException {
    val = 0;
  }
  if (val < 0) {
    val = 0;
  }
  disp[rid]["qty"] = val;
  return val;

}

int getQtyFromRowID(String rid) {
  return getQty("#$rid-qty");
}