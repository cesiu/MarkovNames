/**
 * A sample main to demonstrate use of NameGen.
 * @author Christopher Siu (cesiu)
 * @version 24 Jun 2016
 */

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class GenMain
{
   public static void main(String[] args) throws FileNotFoundException
   {
      boolean isDev = false;
      boolean isSeeded = false;
      String file = null;
      Scanner in = new Scanner(System.in);

      if (args.length < 2) {
         System.out.println("Usage: java GenMain [min] [max] [options]\n" +
                            " -d - prints out the chain as it generates\n" +
                            " -s - seeds the random number generator\n" +
                            " -f - reads initial set of names from a file");
         return;
      }

      if (args.length > 2) {
         for (int i = 2; i < args.length; i++) {
            if (args[i].equals("-d")) {
               isDev = true;
            }
            else if (args[i].equals("-f")) {
               System.out.print("Filename: ");
               file = in.nextLine();
            }
            else if (args[i].equals("-s")) {
               isSeeded = true;
            }
         }
      }

      NameGen gen;
      if (isSeeded) {
         gen = new NameGen(Integer.parseInt(args[0]), 
                           Integer.parseInt(args[1]), 0);
      }
      else {
         gen = new NameGen(Integer.parseInt(args[0]), 
                           Integer.parseInt(args[1]));
      }

      if (file != null) {
         Scanner fileIn = new Scanner(new File(file));
         while (fileIn.hasNext()) {
            String temp = fileIn.nextLine();
            for (int i = 0; i < 50; i++) {
               gen.addName(temp);
            }
         }
      }

      String command = "";
      String lastGen = null;
      do {
         System.out.println("Enter a command:\n" +
                            " add - adds a name to the chain\n" +
                            " gen - generates a name from the chain\n" +
                            " like - adds the last gen to the chain\n" +
                            " ban - removes a letter combo from the chain\n" +
                            " quit - ...quits");
         command = in.nextLine();
         
         if (command.equals("add")) {
            System.out.print("Name: ");
            gen.addName(in.nextLine());
         }
         else if (command.equals("gen")) {
            if (isDev) {
               System.out.println(gen);
            }
            lastGen = gen.getName();
            System.out.println("Generated \"" + lastGen + "\".");
         }
         else if (command.equals("like")) {
            if (lastGen != null) {
               gen.addName(lastGen);
            }
         }
         else if (command.equals("ban")) {
            System.out.print("Combo: ");
            gen.removeName(in.nextLine());
            if (isDev) {
               System.out.println(gen);
            }
         }
      } while (!command.equals("quit"));
   }
}
