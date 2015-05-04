package org.wikidata.wdtk.examples;

/*
 * #%L
 * Wikidata Toolkit Examples
 * %%
 * Copyright (C) 2014 Wikidata Toolkit Developers
 * %%
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * #L%
 */

import java.io.IOException;
import java.io.PrintStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import org.wikidata.wdtk.datamodel.helpers.Datamodel;
import org.wikidata.wdtk.datamodel.interfaces.EntityDocumentProcessor;
import org.wikidata.wdtk.datamodel.interfaces.EntityIdValue;
import org.wikidata.wdtk.datamodel.interfaces.ItemDocument;
import org.wikidata.wdtk.datamodel.interfaces.ItemIdValue;
import org.wikidata.wdtk.datamodel.interfaces.MonolingualTextValue;
import org.wikidata.wdtk.datamodel.interfaces.PropertyDocument;
import org.wikidata.wdtk.datamodel.interfaces.SiteLink;
import org.wikidata.wdtk.datamodel.interfaces.Statement;
import org.wikidata.wdtk.datamodel.interfaces.StatementGroup;
import org.wikidata.wdtk.datamodel.interfaces.TimeValue;
import org.wikidata.wdtk.datamodel.interfaces.Value;
import org.wikidata.wdtk.datamodel.interfaces.ValueSnak;

/**
 * This document processor outputs information on humans that have a gender value or at least a date of birth or date of death
 *
 * @author Markus Kroetzsch
 *
 */
public class GenderIndexProcessor implements EntityDocumentProcessor {
	int itemCount = 0;
	int genderItemCount = 0;
	boolean printedStatus = true;
	List<Person> People = new ArrayList<>();

	/**
	 * Class to store basic information for each site in a simple format.
	 *
	 * @author Markus Kroetzsch
	 *
	 */
	public class Person{
		public ItemIdValue QID;
		public Collection<SiteLink> siteLinks;
		public int birthYear = Integer.MIN_VALUE;
		public int deathYear = Integer.MIN_VALUE;
		public List<EntityIdValue> genderValues = Collections.emptyList();
		public List<EntityIdValue> ethnicGroupValues = Collections.emptyList();
		public List<EntityIdValue> countryOfCitizenshipValues = Collections.emptyList();
		public List<EntityIdValue> placeOfBirthValues = Collections.emptyList();
		

		public Person(ItemIdValue itemIdValue){
			this.QID = itemIdValue;
		}
		
	}

	/**
	 * Class to use for filtering items. This can be changed to analyse a more
	 * specific set of items. Gender information will always be collected, but
	 * it would not be a problem if there was none. For example, you could use
	 * the same code to compare the number of articles about lighthouses
	 * (Q39715) by site; the gender counts would (hopefully) be zero in this
	 * case.
	 */
	static final ItemIdValue filterClass = Datamodel
			.makeWikidataItemIdValue("Q5");

	/**
	 * Main method. Processes the whole dump using this processor and writes the
	 * results to a file. To change which dump file to use and whether to run in
	 * offline mode, modify the settings in {@link ExampleHelpers}.
	 *
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		ExampleHelpers.configureLogging();
		GenderIndexProcessor.printDocumentation();

		GenderIndexProcessor processor = new GenderIndexProcessor();
		ExampleHelpers.processEntitiesFromWikidataDump(processor);
		processor.writeFinalResults();
	}

	/**
	 * Constructor.
	 */
	public GenderIndexProcessor() {
		
	}

	@Override
	public void processItemDocument(ItemDocument itemDocument) {
		this.itemCount++;

		Person person = new Person(itemDocument.getItemId());
		
		person.siteLinks = itemDocument.getSiteLinks().values();

		
		boolean isHuman = false;
		
		

		for (StatementGroup statementGroup : itemDocument.getStatementGroups()) {
			switch (statementGroup.getProperty().getId()) {
			case "P31": // P31 is "instance of"
				isHuman = containsValue(statementGroup, filterClass);
				break;
		
			case "P21": // P21 is "sex or gender"
				person.genderValues = getItemIdValueList(statementGroup);
				break;
			case "P172": // P172 is "ethnic group"
				person.ethnicGroupValues = getItemIdValueList(statementGroup);
				break;
			case "P27": // P27 is "country of citizenship"
				person.countryOfCitizenshipValues = getItemIdValueList(statementGroup);
				break;
			case "P19": // P19 is "place of birth"
				person.placeOfBirthValues = getItemIdValueList(statementGroup);
				break;
				
			case "P569": // P569 is "birth date"
				person.birthYear = getYearValueIfAny(statementGroup);
				break;
			case "P570": // P570 is "death date"
				person.deathYear = getYearValueIfAny(statementGroup);
				break;
			}
		}
		


		if (isHuman) {
			this.genderItemCount++;
			this.printedStatus = false;
			
			People.add(person);

		}


		// Print status once in a while
		if (!this.printedStatus && this.itemCount % 100000 == 0) {
			printStatus();
			this.printedStatus = true;
		}

	}

	@Override
	public void processPropertyDocument(PropertyDocument propertyDocument) {
		// nothing to do for properties
	}

	/**
	 * Writes the results of the processing to a CSV file.
	 */
	public void writeFinalResults() {
		printStatus();
		
		DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
		Date date = new Date();
		String fileName = "gender-index-data-" + dateFormat.format(date) + ".csv";
		
		try (PrintStream out = new PrintStream(
				ExampleHelpers.openExampleFileOuputStream(fileName))) {

			out.print("qid,dob,dod,gender,ethnic_group,citizenship,place_of_birth,site_links");
			out.println();
			for (Person person : People) {
				//qid
				out.print(person.QID.getId());
				out.print(",");
				
				//dob
				out.print(person.birthYear);
				out.print(",");
				
				//dod
				out.print(person.deathYear);
				out.print(",");
				
				//gender
				for(EntityIdValue gender: person.genderValues){
					out.print(gender.getId());
					out.print("|");
				}
				out.print(",");
				
				//ethinc group
				for(EntityIdValue ethnicity: person.ethnicGroupValues){
					out.print(ethnicity.getId());
					out.print("|");
				}
				out.print(",");
				
				//citizenship
				for(EntityIdValue citizenship: person.countryOfCitizenshipValues){
					out.print(citizenship.getId());
					out.print("|");
				}
				out.print(",");
				
				//place of birth
				for(EntityIdValue pob: person.placeOfBirthValues){
					out.print(pob.getId());
					out.print("|");
				}
				out.print(",");
				
				//site_links
				for(SiteLink siteLink : person.siteLinks){
					out.print(siteLink.getSiteKey());
					out.print("|");
				}
				//newline
				out.println();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Prints some basic documentation about this program.
	 */
	public static void printDocumentation() {
		System.out.println(java.lang.Runtime.getRuntime().maxMemory());
		System.out
				.println("********************************************************************");
		System.out.println("*** Wikidata Toolkit: GenderIndexProcessor");
		System.out.println("*** ");
		System.out
				.println("*** This program will download and process dumps from Wikidata.");
		System.out
				.println("*** It will compute the numbers of articles about humans across");
		System.out
				.println("*** Wikimedia projects, and in particular it will count the articles");
		System.out
				.println("*** for each sex/gender. Results will be stored in a CSV file.");
		System.out.println("*** See source code for further details.");
		System.out
				.println("********************************************************************");
	}

	/**
	 * Prints the current status to the system output.
	 */
	private void printStatus() {
		System.out.println("*** Found " + genderItemCount
				+ " items with gender within " + itemCount + " items.");
	}
	
	private int getYearValueIfAny(StatementGroup statementGroup) {
		// Iterate over all statements
		for (Statement s : statementGroup.getStatements()) {
			// Find the main claim and check if it has a value
			if (s.getClaim().getMainSnak() instanceof ValueSnak) {
				Value v = ((ValueSnak) s.getClaim().getMainSnak()).getValue();
				// Check if the value is a TimeValue of sufficient precision
				if (v instanceof TimeValue
						&& ((TimeValue) v).getPrecision() >= TimeValue.PREC_YEAR) {
					return (int) ((TimeValue) v).getYear();
				}
			}
		}

		return Integer.MIN_VALUE;
	}

	/**
	 * Helper method that extracts the list of all {@link ItemIdValue} objects
	 * that are used as values in the given statement group.
	 *
	 * @param statementGroup
	 *            the {@link StatementGroup} to extract the data from
	 * @return the list of values
	 */
	private List<EntityIdValue> getItemIdValueList(StatementGroup statementGroup) {
		List<EntityIdValue> result = new ArrayList<>(statementGroup
				.getStatements().size());

		// Iterate over all statements
		for (Statement s : statementGroup.getStatements()) {
			// Find the main claim and check if it has a value
			if (s.getClaim().getMainSnak() instanceof ValueSnak) {
				Value v = ((ValueSnak) s.getClaim().getMainSnak()).getValue();
				// Check if the value is an ItemIdValue
				if (v instanceof EntityIdValue) {
					result.add((EntityIdValue) v);
				}
			}
		}

		return result;
	}

	/**
	 * Checks if the given group of statements contains the given value as the
	 * value of a main snak of some statement.
	 *
	 * @param statementGroup
	 *            the statement group to scan
	 * @param value
	 *            the value to scan for
	 * @return true if value was found
	 */
	private boolean containsValue(StatementGroup statementGroup, Value value) {
		// Iterate over all statements
		for (Statement s : statementGroup.getStatements()) {
			// Find the main claim and check if it has a value
			if (s.getClaim().getMainSnak() instanceof ValueSnak) {
				Value v = ((ValueSnak) s.getClaim().getMainSnak()).getValue();
				// Check if the value is an ItemIdValue
				if (value.equals(v)) {
					return true;
				}
			}
		}

		return false;
	}


}